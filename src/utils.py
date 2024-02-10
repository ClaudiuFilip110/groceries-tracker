import base64
import json
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        output = base64.b64encode(image_file.read()).decode('utf-8')
        logging.info(f'Encoded image at {image_path}')
        return output


def parse_gpt_response(response):
    try:
        logging.info(f"Parsing GPT4 response: {response}")
        model_used = response['model']
        input_price = (response['usage']['prompt_tokens']) / 1000 * 0.01
        output_price = (response['usage']['completion_tokens']) / 1000 * 0.03
        total_price = input_price + output_price
        content = response['choices'][0]['message']['content']
        json_content = extract_json(content)
        output = json.dumps(json_content)

        logging.info(f"Parsed data: Total price: {total_price}, Items bought: {output}")
        return output
    except Exception as e:
        logging.error(f"Couldn't parse GPT4 response. Error {e}")
        return None


def extract_json(input_string):
    pattern = r'```json\n(.*?)\n```'
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        json_data = match.group(1)
        try:
            return json.loads(json_data)
        except json.JSONDecodeError:
            logging.error("Error decoding the JSON from the GPT4 content")
            return "Invalid JSON format."
    else:
        return "No JSON data found."


def get_current_month():
    now = datetime.now()
    formatted_date = now.strftime("%b %Y").upper()
    return formatted_date


def get_current_month_for_file():
    now = datetime.now()
    formatted_date = now.strftime("%b_%Y").upper()
    return formatted_date


def get_current_day():
    now = datetime.now()
    formatted_date = now.strftime("%d").upper()
    return formatted_date
