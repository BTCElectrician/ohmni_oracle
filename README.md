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

- `main.py`: Main script for processing PDF files
- `drawing_processor.py`: Core logic for processing different types of drawings
- `pdf_processor.py`: Functions for PDF text extraction and data structuring
- `pdf_utils.py`: Additional PDF processing utilities
- `file_utils.py`: Functions for file operations
- `templates/`:
- `room_templates.py`: Functions for processing room data
- `a_rooms_template.json`: Template for architectural room data
- `e_rooms_template.json`: Template for electrical room data

## Usage

Run the script with the following command: python main.py <path_to_job_folder> [<output_folder>]
The script processes all PDF files in the given job folder:
1. Extracts text and tables from PDFs
2. Uses GPT-4-0613 to structure the data into JSON format
3. Generates structured JSON files for all drawings
4. Creates special files for architectural and electrical drawings:
   - `a_rooms_details_floor_[floor_number].json`: for architectural drawings
   - `e_rooms_details_floor_[floor_number].json`: for electrical drawings

Output files are saved in the specified output folder or in an `output` folder within the job folder if not specified.

The script uses asynchronous processing and implements rate limiting for API calls to improve efficiency and manage resources.

## Error Handling

The script implements robust error handling, including:
- JSON validation to ensure proper structure of output data
- Detailed error logging for troubleshooting
- Continuation of processing for other files in case of individual file errors

## Performance

The script uses asynchronous programming to handle multiple files and API calls concurrently, improving performance for large job folders.

## Customization

To add support for new drawing types or modify existing processing:
1. Update the `DRAWING_INSTRUCTIONS` dictionary in `drawing_processor.py` with specific instructions for each drawing type.
2. Modify the corresponding processing logic in `drawing_processor.py` as needed.
3. Update or add JSON templates in the `templates` folder if required.

## Dependencies

- openai
- tqdm
- asyncio
- aiohttp
- pymupdf
- pdfplumber
- (other dependencies as listed in requirements.txt)

Ensure all dependencies are installed before running the script.

## Logging

The script uses Python's built-in logging module to record important events and errors. Log files are stored in the `logs` directory within the output folder.

## Future Improvements

- Implement Pydantic models for more robust data validation and serialization
- Add unit tests for better code reliability
- Consider using async file I/O operations for improved performance

## Folder Structure
ohmni_oracle/
├── main.py
├── drawing_processor.py
├── pdf_processor.py
├── README.md
├── requirements.txt
├── .gitignore
├── templates/
│   ├── room_templates.py
│   ├── a_rooms_template.json
│   └── e_rooms_template.json
├── utils/
│   ├── pdf_utils.py
│   └── file_utils.py
└── logs/
└── room_templates.log