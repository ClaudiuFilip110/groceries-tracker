import logging

import requests

from utils import encode_image

logger = logging.getLogger(__name__)


def gpt4_vision(api_key, image_path, categories):
    try:
        base64_image = encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Extract the items from this receipt, as well as the total in a json format and add the values to one of these categories: {categories}. Return just the JSON, nothing else."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        logging.info(f'GPT4 Completion API returned response: {response}')
        return response.json()

    except Exception as e:
        logging.error(f"Couldn't get GPT4 Completion. Returned error {e}")
        return
