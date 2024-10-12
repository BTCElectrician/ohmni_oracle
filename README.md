# Ohmni Oracle

This project processes various types of architectural and engineering drawings, extracting structured data from PDFs using GPT-4o-mini.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with your OpenAI API key:
OPENAI_API_KEY=your_api_key_here
Copy4. Ensure you have the necessary JSON templates in the `templates` folder:
- `a_rooms_template.json`
- `e_rooms_template.json`

## File Structure

- `main.py`: Main script for processing PDF files
- `utils/`: 
- `pdf_utils.py`: Functions for PDF text extraction
- `file_utils.py`: Functions for file operations
- `templates/`:
- `room_templates.py`: Functions for processing room data
- `a_rooms_template.json`: Template for architectural room data
- `e_rooms_template.json`: Template for electrical room data
- `config/`: Configuration settings (if any)
- `requirements.txt`: List of Python dependencies

## Usage

Run the script with the following command:
python main.py <path_to_job_folder>
Copy
The script processes all PDF files in the given job folder:
1. Extracts text from PDFs
2. Uses GPT-4o-mini to structure the data into JSON format
3. Generates structured JSON files for all drawings
4. Creates special files for architectural and electrical drawings:
   - `a_rooms_details.json`: for all architectural drawings
   - `e_rooms_details.json`: for reflected ceiling plans

Output files are saved in a `parsed_outputs` folder within the job folder.

## Logging

The script logs information and errors to the console. Check the output for processing status and any issues encountered.

## Error Handling

Errors during file processing are logged, and the script continues to process other files in the job folder.

## Performance

The script uses concurrent processing to handle multiple files simultaneously, improving performance for large job folders.

## Customization

To add support for new drawing types or modify existing processing, update the `room_templates.py` file and corresponding JSON templates in the `templates` folder.

## Dependencies

- openai
- tqdm
- python-dotenv
- (other dependencies as listed in requirements.txt)

Ensure all dependencies are installed before running the script.