import pandas as pd
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

def split_csv(file_name, chunk_size, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    chunk_number = 0
    for chunk in pd.read_csv(current_dir + "/" +file_name, chunksize=chunk_size, parse_dates=['candle_begin_time']):
        output_file = os.path.join( f'chunk_{file_name}_{chunk_number}.csv')
        # output_file = os.path.join(output_folder, f'chunk_{file_name}_{chunk_number}.csv')
        chunk.to_csv(output_file, index=False)
        chunk_number += 1

