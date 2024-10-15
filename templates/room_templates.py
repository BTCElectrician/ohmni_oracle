import json
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'room_templates.log')
    
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    console_handler = logging.StreamHandler()
    
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    logging.getLogger('').setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger('')
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def load_template(template_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, f"{template_name}_template.json")
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Template file not found: {template_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {template_path}")
        return {}

def generate_rooms_data(parsed_data, room_type):
    template = load_template(room_type)
    
    rooms_data = {
        "project_name": parsed_data.get('metadata', {}).get('project', ''),
        "floor_number": '',  # Floor number is not provided in the structured data
        "rooms": []
    }
    
    logger.info(f"Generating {room_type} data for project: {rooms_data['project_name']}")
    
    rooms = parsed_data.get('rooms', [])
    if not rooms:
        logger.warning(f"No rooms found in parsed data for {room_type}")
    
    for room in rooms:
        room_id = str(room.get('number', ''))
        room_name = room.get('name', '')
        
        room_data = template.copy()  # Create a copy of the template for each room
        
        if room_type == 'e_rooms':
            room_data['room_id'] = room_id
            room_data['room_name'] = room_name
        elif room_type == 'a_rooms':
            room_data['roomId'] = room_id
            room_data['name'] = room_name
            # Room height is not automatically populated here
        
        rooms_data['rooms'].append(room_data)
    
    logger.info(f"Generated data for {len(rooms_data['rooms'])} rooms")
    return rooms_data

def process_architectural_drawing(parsed_data, file_path, output_folder):
    is_reflected_ceiling = "REFLECTED CEILING PLAN" in file_path.upper()
    
    logger.info(f"Processing file: {file_path}")
    logger.info(f"Is reflected ceiling: {is_reflected_ceiling}")
    
    project_name = parsed_data.get('metadata', {}).get('project', '')
    job_number = parsed_data.get('metadata', {}).get('job_number', '')
    floor_number = ''  # Floor number is not provided in the structured data
    
    logger.info(f"Project: {project_name}, Job Number: {job_number}, Floor: {floor_number}")
    
    e_rooms_data = generate_rooms_data(parsed_data, 'e_rooms')
    a_rooms_data = generate_rooms_data(parsed_data, 'a_rooms')
    
    e_rooms_file = os.path.join(output_folder, f'e_rooms_details_floor_{floor_number}.json')
    a_rooms_file = os.path.join(output_folder, f'a_rooms_details_floor_{floor_number}.json')
    
    with open(e_rooms_file, 'w') as f:
        json.dump(e_rooms_data, f, indent=2)
    
    with open(a_rooms_file, 'w') as f:
        json.dump(a_rooms_data, f, indent=2)
    
    logger.info(f"E-rooms file created: {e_rooms_file}")
    logger.info(f"A-rooms file created: {a_rooms_file}")
    
    return {
        "e_rooms_file": e_rooms_file,
        "a_rooms_file": a_rooms_file,
        "is_reflected_ceiling": is_reflected_ceiling
    }