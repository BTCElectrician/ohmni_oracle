# room_templates.py

import json
import os
import logging

# Set up logging to write to a file
log_file = 'room_templates.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')  # 'w' mode overwrites the file each time

def load_template(template_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, f"{template_name}_template.json")
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Template file not found: {template_path}")
        return {}

def extract_rooms_from_reflected_ceiling(parsed_data):
    rooms = parsed_data.get('architectural_drawing', {}).get('rooms', [])
    return [{"room_number": room.get('room_number', ''), "room_name": room.get('name', '')} for room in rooms]

def generate_rooms_data(parsed_data, room_type):
    template = load_template(room_type)
    rooms_data = {
        "project_name": parsed_data.get('project_name', ''),
        "floor_number": parsed_data.get('floor_number', ''),
        "rooms": []
    }
    
    logging.debug(f"Parsed data: {parsed_data}")
    logging.debug(f"Room type: {room_type}")
    
    rooms = parsed_data.get('rooms', [])
    if not rooms:
        logging.warning(f"No rooms found in parsed data for {room_type}")
    
    for room in rooms:
        logging.debug(f"Processing room: {room}")
        room_data = template.get('rooms', [{}])[0].copy()  # Get the room template safely
        if room_type == 'e_rooms':
            room_data['room_id'] = room.get('code', '')
            room_data['room_name'] = room.get('name', '')
        elif room_type == 'a_rooms':
            room_data['roomId'] = room.get('code', '')
            room_data['name'] = room.get('name', '')
            room_data['ceiling_finish'] = room.get('ceiling_finish', '')
            # Ensure the 'walls' key exists in the template
            if 'walls' not in room_data:
                room_data['walls'] = {'north': '', 'south': '', 'east': '', 'west': ''}
            room_data['ceiling_height'] = ''
            room_data['dimensions'] = ''
        rooms_data['rooms'].append(room_data)
    
    logging.debug(f"Generated rooms data: {rooms_data}")
    return rooms_data

def process_architectural_drawing(parsed_data, file_path, output_folder):
    is_reflected_ceiling = "REFLECTED CEILING PLAN" in file_path.upper()
    
    logging.debug(f"Processing file: {file_path}")
    logging.debug(f"Is reflected ceiling: {is_reflected_ceiling}")
    logging.debug(f"Parsed data: {parsed_data}")
    
    # Extract rooms from the correct location in the parsed data
    all_rooms = parsed_data.get('architectural_drawing', {}).get('rooms', [])
    
    logging.debug(f"All rooms: {all_rooms}")
    
    # Extract project name and floor number
    project_name = parsed_data.get('architectural_drawing', {}).get('project_info', {}).get('project_address', '').split(',')[0].strip()
    if not project_name:
        project_name = parsed_data.get('architectural_drawing', {}).get('title', '').split(' - ')[0]
    job_number = parsed_data.get('architectural_drawing', {}).get('job_number', '')
    floor_number = ''  # You might want to extract this from the filename if available
    
    logging.debug(f"Project name: {project_name}")
    logging.debug(f"Job number: {job_number}")
    logging.debug(f"Floor number: {floor_number}")
    
    e_rooms_data = generate_rooms_data({
        "project_name": project_name,
        "floor_number": floor_number,
        "rooms": all_rooms
    }, 'e_rooms')
    
    a_rooms_data = generate_rooms_data({
        "project_name": project_name,
        "floor_number": floor_number,
        "rooms": all_rooms
    }, 'a_rooms')
    
    e_rooms_file = os.path.join(output_folder, f'e_rooms_details_floor_{floor_number}.json')
    a_rooms_file = os.path.join(output_folder, f'a_rooms_details_floor_{floor_number}.json')
    
    with open(e_rooms_file, 'w') as f:
        json.dump(e_rooms_data, f, indent=2)
    
    with open(a_rooms_file, 'w') as f:
        json.dump(a_rooms_data, f, indent=2)
    
    logging.debug(f"E-rooms file created: {e_rooms_file}")
    logging.debug(f"A-rooms file created: {a_rooms_file}")
    
    return {
        "e_rooms_file": e_rooms_file,
        "a_rooms_file": a_rooms_file,
        "is_reflected_ceiling": is_reflected_ceiling
    }