import os
import json
import sys
import asyncio
import aiohttp
import random
import time
import logging
from datetime import datetime
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm
from templates.room_templates import process_architectural_drawing
from utils.pdf_processor import extract_text_and_tables_from_pdf

# Suppress pdfminer debug output
logging.getLogger('pdfminer').setLevel(logging.ERROR)

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
API_RATE_LIMIT = 60  # Adjust if needed
TIME_WINDOW = 60  # Time window to respect the rate limit

def setup_logging(output_folder):
    log_folder = os.path.join(output_folder, 'logs')
    os.makedirs(log_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_folder, f"process_log_{timestamp}.txt")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    print(f"Logging to: {log_file}")

drawing_types = {
    'Architectural': ['A', 'AD'],
    'Electrical': ['E', 'ED'],
    'Mechanical': ['M', 'MD'],
    'Plumbing': ['P', 'PD'],
    'Site': ['S', 'SD'],
    'Civil': ['C', 'CD'],
    'Low Voltage': ['LV', 'LD'],
    'Fire Alarm': ['FA', 'FD'],
    'Kitchen': ['K', 'KD']
}

def get_drawing_type(filename):
    prefix = os.path.basename(filename).split('.')[0][:2].upper()
    for dtype, prefixes in drawing_types.items():
        if any(prefix.startswith(p.upper()) for p in prefixes):
            return dtype
    return 'General'

async def async_safe_api_call(client, *args, **kwargs):
    retries = 0
    delay = 1  # Initial delay for backoff

    while retries < MAX_RETRIES:
        try:
            return await client.chat.completions.create(*args, **kwargs)
        except Exception as e:
            if "rate limit" in str(e).lower():
                logging.warning(f"Rate limit hit, retrying in {delay} seconds...")
                retries += 1
                delay = min(delay * 2, 60)  # Exponential backoff, with a max delay cap
                await asyncio.sleep(delay + random.uniform(0, 1))  # Adding jitter
            else:
                logging.error(f"API call failed: {e}")
                await asyncio.sleep(RETRY_DELAY)
                retries += 1

    logging.error("Max retries reached for API call")
    raise Exception("Failed to make API call after maximum retries")

async def process_pdf_async(pdf_path, client, output_folder, drawing_type, templates_created):
    file_name = os.path.basename(pdf_path)
    with tqdm(total=100, desc=f"Processing {file_name}", leave=False) as pbar:
        try:
            pbar.update(10)  # Start processing
            raw_content = await extract_text_and_tables_from_pdf(pdf_path)
            
            pbar.update(20)  # Text and tables extracted
            response = await async_safe_api_call(
                client,
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are an expert in parsing {drawing_type} drawings. Structure the following content into a valid JSON format. The content includes both text and tables. Extract key information relevant to this type of drawing. Ensure your entire response is a valid JSON object."},
                    {"role": "user", "content": raw_content}
                ],
                temperature=0.2,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            pbar.update(40)  # API call completed
            structured_json = response.choices[0].message.content
            
            type_folder = os.path.join(output_folder, drawing_type)
            os.makedirs(type_folder, exist_ok=True)
            
            try:
                parsed_json = json.loads(structured_json)
                output_filename = os.path.splitext(file_name)[0] + '_structured.json'
                output_path = os.path.join(type_folder, output_filename)
                
                with open(output_path, 'w') as f:
                    json.dump(parsed_json, f, indent=2)
                
                pbar.update(20)  # JSON saved
                logging.info(f"Successfully processed and saved: {output_path}")
                
                if drawing_type == 'Architectural':
                    result = process_architectural_drawing(parsed_json, pdf_path, type_folder)
                    templates_created['floor_plan'] = True
                    logging.info(f"Created room templates: {result}")
                
                pbar.update(10)  # Processing completed
                return {"success": True, "file": output_path}
            
            except json.JSONDecodeError as e:
                pbar.update(100)  # Ensure bar completes on error
                logging.error(f"JSON parsing error for {pdf_path}: {str(e)}")
                logging.info(f"Raw API response: {structured_json}")
                
                raw_output_filename = os.path.splitext(file_name)[0] + '_raw_response.json'
                raw_output_path = os.path.join(type_folder, raw_output_filename)
                with open(raw_output_path, 'w') as f:
                    f.write(structured_json)
                logging.warning(f"Saved raw API response to {raw_output_path}")
                
                return {"success": False, "error": "Failed to parse JSON", "file": pdf_path}
        
        except Exception as e:
            pbar.update(100)  # Ensure bar completes on error
            logging.error(f"Error processing {pdf_path}: {str(e)}")
            return {"success": False, "error": str(e), "file": pdf_path}

async def process_batch_async(batch, client, output_folder, templates_created):
    tasks = []
    start_time = time.time()
    for index, pdf_file in enumerate(batch):
        if index > 0 and index % API_RATE_LIMIT == 0:
            elapsed = time.time() - start_time
            if elapsed < TIME_WINDOW:
                await asyncio.sleep(TIME_WINDOW - elapsed)
            start_time = time.time()
        
        drawing_type = get_drawing_type(pdf_file)
        tasks.append(process_pdf_async(pdf_file, client, output_folder, drawing_type, templates_created))
    
    return await asyncio.gather(*tasks)

async def process_job_site_async(job_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    pdf_files = [os.path.join(root, file)
                 for root, _, files in os.walk(job_folder)
                 for file in files if file.lower().endswith('.pdf')]
    
    logging.info(f"Found {len(pdf_files)} PDF files in {job_folder}")
    
    if not pdf_files:
        logging.warning("No PDF files found. Please check the input folder.")
        return
    
    templates_created = {"floor_plan": False}
    
    batch_size = 10
    total_batches = (len(pdf_files) + batch_size - 1) // batch_size

    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    all_results = []
    with tqdm(total=len(pdf_files), desc="Overall Progress") as overall_pbar:
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i+batch_size]
            logging.info(f"Processing batch {i//batch_size + 1} of {total_batches}")
            
            batch_results = await process_batch_async(batch, client, output_folder, templates_created)
            all_results.extend(batch_results)
            
            successes = [r for r in batch_results if r['success']]
            failures = [r for r in batch_results if not r['success']]
            
            overall_pbar.update(len(batch))
            logging.info(f"Batch completed. Successes: {len(successes)}, Failures: {len(failures)}")
            
            for failure in failures:
                logging.error(f"Failed to process {failure['file']}: {failure['error']}")

    successes = [r for r in all_results if r['success']]
    failures = [r for r in all_results if not r['success']]
    
    logging.info(f"Processing complete. Total successes: {len(successes)}, Total failures: {len(failures)}")
    
    if failures:
        logging.warning("Failures:")
        for failure in failures:
            logging.warning(f"  {failure['file']}: {failure['error']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_folder> [output_folder]")
        sys.exit(1)
    
    job_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else os.path.join(job_folder, "output")
    
    if not os.path.exists(job_folder):
        print(f"Error: Input folder '{job_folder}' does not exist.")
        sys.exit(1)
    
    setup_logging(output_folder)
    
    logging.info(f"Processing files from: {job_folder}")
    logging.info(f"Output will be saved to: {output_folder}")
    
    asyncio.run(process_job_site_async(job_folder, output_folder))