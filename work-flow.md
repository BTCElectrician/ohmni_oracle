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
