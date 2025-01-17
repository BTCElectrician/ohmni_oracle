================================================
File: README.md
================================================
# Ohmni Oracle

This project processes various types of architectural and engineering drawings, including electrical, mechanical, plumbing, and architectural documents. It extracts structured data from PDFs using gpt-4o-mini.  

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with your OpenAI API key: OPENAI_API_KEY=your_api_key_here
4. Ensure you have the necessary JSON templates in the `templates` folder:
- `a_rooms_template.json`
- `e_rooms_template.json`

## File Structure

- `main.py`: Main script for processing PDF files and coordinating async operations
- `.env`: Environment variables configuration
- `.gitignore`: Git ignore rules
- `.cursorrules`: Cursor editor configuration
- `git-best-practices-guide.md`: Git workflow guidelines
- `requirements.txt`: Project dependencies

### Config
- `config/.gitignore`: Config-specific git ignore rules
- `config/settings.py`: Environment variables and configuration settings

### Templates
- `templates/room_templates.py`: Functions for processing room data
- `templates/a_rooms_template.json`: Template for architectural room data
- `templates/e_rooms_template.json`: Template for electrical room data

### Utils
- `utils/__init__.py`: Package initialization
- `utils/drawing_processor.py`: Drawing-specific processing logic and GPT prompts
- `utils/file_utils.py`: File system operations and folder traversal
- `utils/pdf_processor.py`: PDF text extraction and processing functions
- `utils/pdf_utils.py`: PDF processing utilities (image extraction, metadata)

## Folder Structure
ohmni_oracle/
├── config/
│   ├── .gitignore
│   └── settings.py
├── path/to/your/output/
├── templates/
│   ├── __pycache__/
│   ├── a_rooms_template.json
│   ├── e_rooms_template.json
│   └── room_templates.py
├── utils/
│   ├── __init__.py
│   ├── drawing_processor.py
│   ├── file_utils.py
│   ├── pdf_processor.py
│   └── pdf_utils.py
├── venv/
├── .cursorrules
├── .env
├── .gitignore
├── git-best-practices-guide.md
├── main.py
├── README.md
└── requirements.txt

================================================
File: git-best-practices-guide.md
================================================
# Comprehensive Git Best Practices Guide

## Table of Contents
1. [Understanding Git and Version Control](#1-understanding-git-and-version-control)
2. [Setting Up Your Project](#2-setting-up-your-project)
3. [Best Practices for Commits](#3-best-practices-for-commits)
4. [Branching Strategy](#4-branching-strategy)
5. [Collaboration and Remote Repositories](#5-collaboration-and-remote-repositories)
6. [Handling Mistakes](#6-handling-mistakes)
7. [Advanced Git Features](#7-advanced-git-features)
8. [Maintaining Your Repository](#8-maintaining-your-repository)
9. [Best Practices for Python Projects](#9-best-practices-for-python-projects)
10. [Continuous Learning](#10-continuous-learning)

## 1. Understanding Git and Version Control

Git is a distributed version control system that allows you to track changes in your code, collaborate with others, and maintain different versions of your project. Key concepts include:

- **Repository**: A container for your project, including all files and their revision history.
- **Commit**: A snapshot of your project at a specific point in time.
- **Branch**: An independent line of development.
- **Remote**: A version of your project hosted on a server (like GitHub).

## 2. Setting Up Your Project

Before you start coding:

a. Initialize a Git repository:
   ```
   git init
   ```

b. Create a .gitignore file immediately:
   ```
   touch .gitignore
   ```

c. Edit .gitignore to exclude common unnecessary files:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *.so

   # Virtual Environment
   venv/
   env/
   *.venv
   
   # IDEs and Editors
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS generated files
   .DS_Store
   Thumbs.db

   # Project-specific
   *.log
   *.sqlite3
   ```

d. Commit your .gitignore file:
   ```
   git add .gitignore
   git commit -m "Initial commit: Add .gitignore"
   ```

## 3. Best Practices for Commits

a. Commit early and often:
   - Make small, focused commits that do one thing.
   - This makes it easier to understand changes and revert if necessary.

b. Write meaningful commit messages:
   - Use the imperative mood: "Add feature" not "Added feature"
   - First line: Short (50 chars or less) summary
   - Followed by a blank line
   - Then a more detailed explanation if necessary

c. Before committing:
   - Always run `git status` to see what changes you're about to commit
   - Use `git diff` to review your changes

d. Use `git add -p` to stage changes in hunks, allowing you to make more granular commits

## 4. Branching Strategy

a. Use branches for new features or bug fixes:
   ```
   git checkout -b feature/new-login-system
   ```

b. Keep your main (or master) branch stable

c. Merge or rebase frequently to stay up-to-date with the main branch

d. Delete branches after merging:
   ```
   git branch -d feature/new-login-system
   ```

## 5. Collaboration and Remote Repositories

a. Clone repositories:
   ```
   git clone https://github.com/username/repository.git
   ```

b. Add remotes:
   ```
   git remote add origin https://github.com/username/repository.git
   ```

c. Push your changes:
   ```
   git push origin main
   ```

d. Pull changes from others:
   ```
   git pull origin main
   ```

## 6. Handling Mistakes

a. Undo last commit (keeping changes):
   ```
   git reset HEAD~1
   ```

b. Amend last commit:
   ```
   git commit --amend
   ```

c. Undo staged changes:
   ```
   git reset HEAD <file>
   ```

d. Discard local changes:
   ```
   git checkout -- <file>
   ```

## 7. Advanced Git Features

a. Stashing changes:
   ```
   git stash
   git stash pop
   ```

b. Interactive rebase to clean up commit history:
   ```
   git rebase -i HEAD~3
   ```

c. Use tags for releases:
   ```
   git tag -a v1.0 -m "Version 1.0"
   ```

## 8. Maintaining Your Repository

a. Regularly update your .gitignore if you start using new tools or generating new types of files

b. Use `git clean -n` to see what untracked files would be removed (use -f to actually remove them)

c. Periodically run `git gc` to clean up and optimize your local repository

## 9. Best Practices for Python Projects

a. Use virtual environments for every project

b. Generate a requirements.txt file:
   ```
   pip freeze > requirements.txt
   ```

c. Include the requirements.txt in your repository, but not the virtual environment itself

## 10. Continuous Learning

a. Read Git documentation regularly

b. Practice with online Git tutorials and sandboxes

c. Contribute to open-source projects to see how larger teams use Git

Remember, becoming proficient with Git is a journey. Don't be afraid to make mistakes – that's how you learn. Always keep a backup of your important work, especially when trying new Git commands.

By following these practices, you'll maintain a clean, efficient, and professional Git repository. This will make your development process smoother, facilitate collaboration, and showcase your growing skills as a software developer.



================================================
File: main.py
================================================
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
from utils.drawing_processor import process_drawing

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
            structured_json = await process_drawing(raw_content, drawing_type, client)
            
            pbar.update(40)  # API call completed
            
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

================================================
File: requirements.txt
================================================
aiohappyeyeballs==2.4.1
aiohttp==3.10.6
aiosignal==1.3.1
annotated-types==0.7.0
anyio==4.6.0
attrs==24.2.0
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.3.2
cryptography==43.0.1
distro==1.9.0
frozenlist==1.4.1
h11==0.14.0
httpcore==1.0.5
httpx==0.27.2
idna==3.10
jiter==0.5.0
multidict==6.1.0
openai==1.50.0
pdfminer.six==20231228
pdfplumber==0.11.4
pillow==10.4.0
pycparser==2.22
pydantic==2.9.2
pydantic_core==2.23.4
PyMuPDF==1.24.11
pypdfium2==4.30.0
python-dotenv==1.0.1
requests==2.32.3
sniffio==1.3.1
tqdm==4.66.5
typing_extensions==4.12.2
urllib3==2.2.3
Wand==0.6.13
yarl==1.12.1


================================================
File: work-flow.md
================================================
# Ohmni Oracle System Workflow

## 1. Data Flow Diagram
```
PDF Input Files
       ↓
File Detection & Classification
       ↓
Text/Table Extraction (pdf_processor.py)
       ↓
Drawing Type Classification
       ↓
GPT Processing Pipeline
       ↓
JSON Structure Generation
       ↓
Template Application
       ↓
Output File Generation
       ↓
Final JSON Storage
```

## 2. Component Interaction Flow

### Main Orchestration (main.py)
```
process_job_site_async
    ↓
traverse_job_folder (file_utils.py)
    ↓
get_drawing_type (file_utils.py)
    ↓
process_batch_async
    ↓
process_pdf_async
```

### Drawing Processing Pipeline
```
extract_text_and_tables_from_pdf (pdf_processor.py)
    ↓
process_drawing (drawing_processor.py)
    ↓
GPT Processing (Type-specific)
    ├─→ Architectural: Room extraction, dimensions
    ├─→ Electrical: Panel schedules, circuits
    ├─→ Mechanical: Equipment schedules
    └─→ Plumbing: Fixture schedules
    ↓
Template Application (room_templates.py)
    ↓
JSON Output Generation
```

## 3. File Purpose Map

### Core Processing Files
- **main.py**
  - Entry point
  - Orchestrates async processing
  - Reference: 

```140:182:main.py
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
```


- **utils/drawing_processor.py**
  - Handles GPT interactions
  - Drawing-specific prompts
  - Reference:

```23:49:utils/drawing_processor.py
async def process_drawing(raw_content: str, drawing_type: str, client: AsyncOpenAI):
    system_message = f"""
    Parse this {drawing_type} drawing/schedule into a structured JSON format. Guidelines:
    1. For text: Extract key information, categorize elements.
    2. For tables: Preserve structure, use nested arrays/objects.
    3. Create a hierarchical structure, use consistent key names.
    4. Include metadata (drawing number, scale, date) if available.
    5. {DRAWING_INSTRUCTIONS.get(drawing_type, DRAWING_INSTRUCTIONS["General"])}
    6. For all drawing types, if room information is present, always include a 'rooms' array in the JSON output, with each room having at least 'number' and 'name' fields.
    Ensure the entire response is a valid JSON object.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": raw_content}
            ],
            temperature=0.2,
            max_tokens=16000,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing {drawing_type} drawing: {str(e)}")
        raise
```


- **utils/pdf_processor.py**
  - PDF text/table extraction
  - Content preprocessing
  - Reference:

```6:41:utils/pdf_processor.py
async def extract_text_and_tables_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    all_content = ""
    for page in doc:
        text = page.get_text()
        all_content += "TEXT:\n" + text + "\n"
        
        tables = page.find_tables()
        for table in tables:
            all_content += "TABLE:\n"
            markdown = table.to_markdown()
            all_content += markdown + "\n"
    
    return all_content

async def structure_panel_data(client: AsyncOpenAI, raw_content: str) -> dict:
    prompt = f"""
    You are an expert in electrical engineering and panel schedules. 
    Please structure the following content from an electrical panel schedule into a valid JSON format. 
    The content includes both text and tables. Extract key information such as panel name, voltage, amperage, circuits, and any other relevant details.
    Pay special attention to the tabular data, which represents circuit information.
    Ensure your entire response is a valid JSON object.
    Raw content:
    {raw_content}
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that structures electrical panel data into JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```


### Support Components
- **utils/file_utils.py**
  - File system operations
  - Drawing type detection
  - Reference:

```7:40:utils/file_utils.py
def get_drawing_type(file_path: str, job_folder: str) -> Optional[str]:
    """
    Determine the drawing type based on the file path and job folder.
    
    Args:
    file_path (str): The full path to the PDF file.
    job_folder (str): The root job folder path.

    Returns:
    Optional[str]: The determined drawing type, or None if it can't be determined.
    """
    relative_path = os.path.relpath(file_path, job_folder)
    path_components = relative_path.lower().split(os.sep)

    drawing_types = {
        "architectural": ["architectural", "arch", "a"],
        "electrical": ["electrical", "elec", "e"],
        "mechanical": ["mechanical", "mech", "m"],
        "plumbing": ["plumbing", "plumb", "p"],
        "structural": ["structural", "struct", "s"],
        "kitchen": ["kitchen", "kit", "k"],
        "civil": ["civil", "civ", "c"],
        "fire_protection": ["fire protection", "fire", "fp"],
        "low_voltage": ["low voltage", "low-voltage", "lv"],
        # Add more drawing types here as needed
    }

    for component in path_components:
        for drawing_type, keywords in drawing_types.items():
            if any(keyword in component for keyword in keywords):
                return drawing_type

    logger.warning(f"Could not determine drawing type for {file_path}")
    return None
```


- **utils/pdf_utils.py**
  - PDF metadata extraction
  - Image processing
  - Reference:

```9:44:utils/pdf_utils.py
def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    str: The extracted text from the PDF.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    logger.info(f"Starting text extraction for {file_path}")
    try:
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"Successfully opened {file_path}")
            text = ""
            for i, page in enumerate(pdf.pages):
                logger.info(f"Processing page {i+1} of {len(pdf.pages)}")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    logger.warning(f"No text extracted from page {i+1}")
        
        if not text:
            logger.warning(f"No text extracted from {file_path}")
        else:
            logger.info(f"Successfully extracted text from {file_path}")
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        raise
```


### Templates and Configuration
- **templates/room_templates.py**
  - Template loading/application
  - Room data structuring
  - Reference:

```17:53:templates/room_templates.py
def generate_rooms_data(parsed_data, room_type):
    template = load_template(room_type)
    
    metadata = parsed_data.get('metadata', {})
    
    rooms_data = {
        "metadata": metadata,
        "project_name": metadata.get('project', ''),
        "floor_number": '',
        "rooms": []
    }
    
    parsed_rooms = parsed_data.get('rooms', [])
    
    if not parsed_rooms:
        print(f"No rooms found in parsed data for {room_type}.")
        return rooms_data

    for parsed_room in parsed_rooms:
        room_number = str(parsed_room.get('number', ''))
        room_name = parsed_room.get('name', '')
        
        if not room_number or not room_name:
            print(f"Skipping room with incomplete data: {parsed_room}")
            continue
        
        room_data = template.copy()
        room_data['room_id'] = f"Room_{room_number}"
        room_data['room_name'] = f"{room_name}_{room_number}"
        
        # Copy all fields from parsed_room to room_data
        for key, value in parsed_room.items():
            if key not in ['number', 'name']:  # Avoid duplicating number and name
                room_data[key] = value
        
        rooms_data['rooms'].append(room_data)
    
```


- **config/settings.py**
  - Environment configuration
  - API key management

### Data Transformations
1. **PDF → Raw Text/Tables**
   - Handled by: pdf_processor.py
   - Uses: pdfplumber, PyMuPDF

2. **Raw Content → Structured JSON**
   - Handled by: drawing_processor.py
   - Uses: GPT-4o-mini model
   - Drawing-specific prompts

3. **Structured JSON → Template-based Output**
   - Handled by: room_templates.py
   - Templates: a_rooms_template.json, e_rooms_template.json

4. **Final Output**
   - Organized by drawing type
   - Includes metadata
   - Searchable JSON format

### Processing Triggers
- **File Detection**: Triggered by file extension (.pdf)
- **Drawing Classification**: Triggered by filename prefix/path
- **GPT Processing**: Triggered after successful text extraction
- **Template Application**: Triggered for specific drawing types (Architectural, Electrical)
- **Output Generation**: Triggered after successful processing

This workflow ensures efficient processing of various drawing types while maintaining modularity and scalability in the system architecture.


================================================
File: config/settings.py
================================================
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

================================================
File: config/.gitignore
================================================
# .gitignore

# Environment variables
.env

# Python bytecode
__pycache__/
*.py[cod]

# Virtual environment
venv/
env/

# IDE settings
.vscode/
.idea/

# Operating system files
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp

# Output directory
parsed_outputs/

================================================
File: templates/a_rooms_template.json
================================================
{
    "room_id": "",
    "room_name": "",
    "walls": {
      "north": "",
      "south": "",
      "east": "",
      "west": ""
    },
    "ceiling_height": "",
    "dimensions": ""
  }

================================================
File: templates/e_rooms_template.json
================================================
{
  "room_id": "",
  "room_name": "",
  "circuits": {
    "lighting": [],
    "power": []
  },
  "light_fixtures": {
    "fixture_ids": [],
    "fixture_count": {}
  },
  "outlets": {
    "regular_outlets": 0,
    "controlled_outlets": 0
  },
  "data": 0,
  "floor_boxes": 0,
  "mechanical_equipment": [],
  "switches": {
    "type": "",
    "model": "",
    "dimming": ""
  }
}

================================================
File: templates/room_templates.py
================================================
import json
import os

def load_template(template_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, f"{template_name}_template.json")
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {template_path}")
        return {}

def generate_rooms_data(parsed_data, room_type):
    template = load_template(room_type)
    
    metadata = parsed_data.get('metadata', {})
    
    rooms_data = {
        "metadata": metadata,
        "project_name": metadata.get('project', ''),
        "floor_number": '',
        "rooms": []
    }
    
    parsed_rooms = parsed_data.get('rooms', [])
    
    if not parsed_rooms:
        print(f"No rooms found in parsed data for {room_type}.")
        return rooms_data

    for parsed_room in parsed_rooms:
        room_number = str(parsed_room.get('number', ''))
        room_name = parsed_room.get('name', '')
        
        if not room_number or not room_name:
            print(f"Skipping room with incomplete data: {parsed_room}")
            continue
        
        room_data = template.copy()
        room_data['room_id'] = f"Room_{room_number}"
        room_data['room_name'] = f"{room_name}_{room_number}"
        
        # Copy all fields from parsed_room to room_data
        for key, value in parsed_room.items():
            if key not in ['number', 'name']:  # Avoid duplicating number and name
                room_data[key] = value
        
        rooms_data['rooms'].append(room_data)
    
    return rooms_data

def process_architectural_drawing(parsed_data, file_path, output_folder):
    is_reflected_ceiling = "REFLECTED CEILING PLAN" in file_path.upper()
    
    project_name = parsed_data.get('metadata', {}).get('project', '')
    job_number = parsed_data.get('metadata', {}).get('job_number', '')
    floor_number = ''  # If floor number is available in the future, extract it here
    
    e_rooms_data = generate_rooms_data(parsed_data, 'e_rooms')
    a_rooms_data = generate_rooms_data(parsed_data, 'a_rooms')
    
    e_rooms_file = os.path.join(output_folder, f'e_rooms_details_floor_{floor_number}.json')
    a_rooms_file = os.path.join(output_folder, f'a_rooms_details_floor_{floor_number}.json')
    
    with open(e_rooms_file, 'w') as f:
        json.dump(e_rooms_data, f, indent=2)
    
    with open(a_rooms_file, 'w') as f:
        json.dump(a_rooms_data, f, indent=2)
    
    return {
        "e_rooms_file": e_rooms_file,
        "a_rooms_file": a_rooms_file,
        "is_reflected_ceiling": is_reflected_ceiling
    }

if __name__ == "__main__":
    # This block is for testing purposes. You can remove it if not needed.
    test_file_path = "path/to/your/test/file.json"
    test_output_folder = "path/to/your/test/output/folder"
    
    with open(test_file_path, 'r') as f:
        test_parsed_data = json.load(f)
    
    result = process_architectural_drawing(test_parsed_data, test_file_path, test_output_folder)
    print(result)

================================================
File: utils/drawing_processor.py
================================================
from openai import AsyncOpenAI

DRAWING_INSTRUCTIONS = {
    "Electrical": "Focus on panel schedules, circuit info, equipment schedules with electrical characteristics, and installation notes.",
    "Mechanical": "Capture equipment schedules, HVAC details (CFM, capacities), and installation instructions.",
    "Plumbing": "Include fixture schedules, pump details, water heater specs, pipe sizing, and system instructions.",
    "Architectural": """
    Extract and structure the following information:
    1. Room details: Create a 'rooms' array with objects for each room, including:
       - 'number': Room number (as a string)
       - 'name': Room name
       - 'finish': Ceiling finish
       - 'height': Ceiling height
    2. Room finish schedules
    3. Door/window details
    4. Wall types
    5. Architectural notes
    Ensure all rooms are captured and properly structured in the JSON output.
    """,
    "General": "Organize all relevant data into logical categories based on content type."
}

async def process_drawing(raw_content: str, drawing_type: str, client: AsyncOpenAI):
    system_message = f"""
    Parse this {drawing_type} drawing/schedule into a structured JSON format. Guidelines:
    1. For text: Extract key information, categorize elements.
    2. For tables: Preserve structure, use nested arrays/objects.
    3. Create a hierarchical structure, use consistent key names.
    4. Include metadata (drawing number, scale, date) if available.
    5. {DRAWING_INSTRUCTIONS.get(drawing_type, DRAWING_INSTRUCTIONS["General"])}
    6. For all drawing types, if room information is present, always include a 'rooms' array in the JSON output, with each room having at least 'number' and 'name' fields.
    Ensure the entire response is a valid JSON object.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": raw_content}
            ],
            temperature=0.2,
            max_tokens=16000,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing {drawing_type} drawing: {str(e)}")
        raise

================================================
File: utils/file_utils.py
================================================
import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

def get_drawing_type(file_path: str, job_folder: str) -> Optional[str]:
    """
    Determine the drawing type based on the file path and job folder.
    
    Args:
    file_path (str): The full path to the PDF file.
    job_folder (str): The root job folder path.

    Returns:
    Optional[str]: The determined drawing type, or None if it can't be determined.
    """
    relative_path = os.path.relpath(file_path, job_folder)
    path_components = relative_path.lower().split(os.sep)

    drawing_types = {
        "architectural": ["architectural", "arch", "a"],
        "electrical": ["electrical", "elec", "e"],
        "mechanical": ["mechanical", "mech", "m"],
        "plumbing": ["plumbing", "plumb", "p"],
        "structural": ["structural", "struct", "s"],
        "kitchen": ["kitchen", "kit", "k"],
        "civil": ["civil", "civ", "c"],
        "fire_protection": ["fire protection", "fire", "fp"],
        "low_voltage": ["low voltage", "low-voltage", "lv"],
        # Add more drawing types here as needed
    }

    for component in path_components:
        for drawing_type, keywords in drawing_types.items():
            if any(keyword in component for keyword in keywords):
                return drawing_type

    logger.warning(f"Could not determine drawing type for {file_path}")
    return None

def traverse_job_folder(job_folder: str) -> List[str]:
    """
    Traverse the job folder and collect all PDF files.

    Args:
    job_folder (str): The root job folder path to traverse.

    Returns:
    List[str]: A list of full file paths to all PDF files found.
    """
    pdf_files = []
    try:
        for root, _, files in os.walk(job_folder):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        logger.info(f"Found {len(pdf_files)} PDF files in {job_folder}")
    except Exception as e:
        logger.error(f"Error traversing job folder {job_folder}: {str(e)}")
    return pdf_files

def cleanup_temporary_files(output_folder: str) -> None:
    """
    Clean up any temporary files created during processing.

    Args:
    output_folder (str): The folder containing output files.
    """
    # Implement cleanup logic here if needed
    pass

def get_project_name(job_folder: str) -> str:
    """
    Extract the project name from the job folder path.

    Args:
    job_folder (str): The root job folder path.

    Returns:
    str: The project name.
    """
    return os.path.basename(job_folder)

================================================
File: utils/pdf_processor.py
================================================
import pymupdf
import json
import os
from openai import AsyncOpenAI

async def extract_text_and_tables_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    all_content = ""
    for page in doc:
        text = page.get_text()
        all_content += "TEXT:\n" + text + "\n"
        
        tables = page.find_tables()
        for table in tables:
            all_content += "TABLE:\n"
            markdown = table.to_markdown()
            all_content += markdown + "\n"
    
    return all_content

async def structure_panel_data(client: AsyncOpenAI, raw_content: str) -> dict:
    prompt = f"""
    You are an expert in electrical engineering and panel schedules. 
    Please structure the following content from an electrical panel schedule into a valid JSON format. 
    The content includes both text and tables. Extract key information such as panel name, voltage, amperage, circuits, and any other relevant details.
    Pay special attention to the tabular data, which represents circuit information.
    Ensure your entire response is a valid JSON object.
    Raw content:
    {raw_content}
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that structures electrical panel data into JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

async def process_pdf(pdf_path: str, output_folder: str, client: AsyncOpenAI):
    print(f"Processing PDF: {pdf_path}")
    raw_content = await extract_text_and_tables_from_pdf(pdf_path)
    
    structured_data = await structure_panel_data(client, raw_content)
    
    panel_name = structured_data.get('panel_name', 'unknown_panel').replace(" ", "_").lower()
    filename = f"{panel_name}_electric_panel.json"
    filepath = os.path.join(output_folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print(f"Saved structured panel data: {filepath}")
    return raw_content, structured_data

================================================
File: utils/pdf_utils.py
================================================
# pdf_utils.py

import pdfplumber
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    str: The extracted text from the PDF.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    logger.info(f"Starting text extraction for {file_path}")
    try:
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"Successfully opened {file_path}")
            text = ""
            for i, page in enumerate(pdf.pages):
                logger.info(f"Processing page {i+1} of {len(pdf.pages)}")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    logger.warning(f"No text extracted from page {i+1}")
        
        if not text:
            logger.warning(f"No text extracted from {file_path}")
        else:
            logger.info(f"Successfully extracted text from {file_path}")
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        raise

def extract_images(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract images from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    List[Dict[str, Any]]: A list of dictionaries containing image information.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    try:
        images = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                for image in page.images:
                    images.append({
                        'page': i + 1,
                        'bbox': image['bbox'],
                        'width': image['width'],
                        'height': image['height'],
                        'type': image['type']
                    })
        
        logger.info(f"Extracted {len(images)} images from {file_path}")
        return images
    except Exception as e:
        logger.error(f"Error extracting images from {file_path}: {str(e)}")
        raise

def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get metadata from a PDF file.
    
    Args:
    file_path (str): The path to the PDF file.
    
    Returns:
    Dict[str, Any]: A dictionary containing the PDF metadata.
    
    Raises:
    Exception: If there's an error in opening or processing the PDF.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            metadata = pdf.metadata
        logger.info(f"Successfully extracted metadata from {file_path}")
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {str(e)}")
        raise


Directory structure:
└── btcelectrician-ohmni_oracle/
    ├── README.md
    ├── git-best-practices-guide.md
    ├── main.py
    ├── requirements.txt
    ├── work-flow.md
    ├── .cursorrules
    ├── config/
    │   ├── settings.py
    │   └── .gitignore
    ├── path/
    │   ├── .DS_Store
    │   └── to/
    │       ├── .DS_Store
    │       └── your/
    │           ├── .DS_Store
    │           └── output/
    │               └── .DS_Store
    ├── templates/
    │   ├── a_rooms_template.json
    │   ├── e_rooms_template.json
    │   ├── room_templates.py
    │   └── __pycache__/
    └── utils/
        ├── __init__.py
        ├── drawing_processor.py
        ├── file_utils.py
        ├── pdf_processor.py
        └── pdf_utils.py
