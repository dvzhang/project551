import pandas as pd
import os

def insert_sort(data, column):
    for i in range(1, len(data)):
        key_item = data.iloc[i]
        j = i - 1
        while j >= 0 and data.iloc[j][column] > key_item[column]:
            data.iloc[j + 1] = data.iloc[j]
            j -= 1
        data.iloc[j + 1] = key_item
    return data


def map_function(chunk_file, table_name, parsed_sql, output_folder):
    data = pd.read_csv(chunk_file, parse_dates=['candle_begin_time'])
    if parsed_sql['where']:
        data = data.query(parsed_sql['where'])
    if parsed_sql['select']:
        data = data[parsed_sql['select']]
    if parsed_sql['order_by']:
        data = insert_sort(data, parsed_sql['order_by'])
    data['source_table'] = table_name  # 添加表名标识
    output_file = os.path.join(output_folder, f'sorted_{table_name}_{os.path.basename(chunk_file)}')
    data.to_csv(output_file, index=False)

