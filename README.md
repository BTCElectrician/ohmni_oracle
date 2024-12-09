# Ohmni Oracle

This project processes various types of architectural and engineering drawings, including electrical, mechanical, plumbing, and architectural documents. It extracts structured data from PDFs using gpt-4o-mini.  TESTING TO SEE IF THIS WORKS

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