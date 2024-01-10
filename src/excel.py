import json
import logging
import os

import pandas as pd
from openpyxl import load_workbook

from utils import get_current_month, get_current_day, get_current_month_for_file

logger = logging.getLogger(__name__)


def get_categories(excel_path):
    # TODO: Add error handling and logging
    sheet_name = get_current_month()
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    days = get_payments_table(df)
    return list(days.index)


def get_payments_table(df):
    try:
        indices = list(df.iloc[12:22, 0])
        orig_column_names = list(df.iloc[11, 1:32].index)
        column_names = list(df.iloc[11, 1:32].apply(lambda x: int(x)))

        dic = {}
        for old, new in zip(orig_column_names, column_names):
            dic[old] = new

        days = df.iloc[12:22, 1:32]
        days = days.rename(columns=dic)
        days.index = indices
        days = days.fillna(0.0)
        logging.info('Successfully extracted day by day payments table')
        return days
    except Exception as e:
        logging.error(f"Exception trying to get payments table: {e}")
        return


def write_to_excel(excel_path, sheet_name, df):
    try:
        range_rows = range(12, 22)
        range_cols = range(1, 32)
        workbook = load_workbook(filename=excel_path)
        sheet = workbook[sheet_name]

        print(df.iloc[range_rows, range_cols])
        for i in range_rows:
            for j in range_cols:
                sheet.cell(i + 2, j + 1, value=df.iloc[i, j])
                # TODO: Handle path better
        filename = f'{os.getcwd()}/../data/budget/{get_current_month_for_file()}.xlsx'
        workbook.save(filename=filename)
        logging.info(f'Successfully saved new workbook at {filename}')

    except Exception as e:
        # TODO: Better exception handling. Everywhere
        logging.error(f"Exception while writing data to Excel, {e}")
        return


def add_to_excel(excel_path, dic):
    sheet_name = get_current_month()
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        logging.info('Successfully read Excel file')

        days = get_payments_table(df)
        if days is None:
            return

        today = int(get_current_day())
        dic = json.loads(dic)
        for item in dic['items']:
            # TODO: get data from receipt, instead of just `today`
            days.loc[item['category'], today] += float(item['price'].replace('£', ''))

        df.iloc[12:22, 1:32] = days
        if write_to_excel(excel_path, sheet_name, df):
            return True
        return

    except Exception as e:
        logging.error(f"Couldn't add data to excel: {e}")
        return
