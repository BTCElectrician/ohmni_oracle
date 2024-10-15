import logging
from openai import AsyncOpenAI

DRAWING_INSTRUCTIONS = {
    "Electrical": "Focus on panel schedules, circuit info, equipment schedules with electrical characteristics, and installation notes.",
    "Mechanical": "Capture equipment schedules, HVAC details (CFM, capacities), and installation instructions.",
    "Plumbing": "Include fixture schedules, pump details, water heater specs, pipe sizing, and system instructions.",
    "Architectural": "Extract room finish schedules, door/window details, wall types, and architectural notes.",
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
            max_tokens=16000,  # Updated to a higher value, but still within the model's limit
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error processing {drawing_type} drawing: {str(e)}")
        raise