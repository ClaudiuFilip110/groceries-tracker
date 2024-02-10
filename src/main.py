import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from excel import get_categories, add_to_excel
from openai import gpt4_vision
from utils import parse_gpt_response

load_dotenv()

Path('../logs/').mkdir(exist_ok=True)
logging.basicConfig(filename=f'../logs/{time.strftime("%d-%m-%Y")}.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

api_key = os.getenv('OPENAI_KEY')
excel_path = os.getenv('EXCEL_PATH')
image_path = Path("../data/tesco_4.jpeg")
categories = get_categories(excel_path)


def main():
    # TODO: Add console params
    with tqdm(total=3, desc='Analyze the receipt, extract the data and add the Excel') as pbar:
        response = gpt4_vision(api_key, image_path, categories)
        pbar.update(1)

        if response is None:
            return
        output = parse_gpt_response(response)
        logging.info(f'Caching GPT response: {output}')
        pbar.update(1)

        # TODO: Handle returns consistently. Sometimes returns None, sometimes str
        if add_to_excel(excel_path, output):
            logging.info('Data added back to Excel successfully')
        else:
            logging.error('Error returned while adding data to Excel. Check logs')
        pbar.update(1)


if __name__ == "__main__":
    main()
