import pandas as pd
import glob
import os

# shuffle.py
def shuffle_data(sorted_files_pattern, output_folder):
    output_file = os.path.join(output_folder, 'shuffled_data.csv')
    all_data = pd.concat([pd.read_csv(file) for file in glob.glob(sorted_files_pattern)], ignore_index=True)
    all_data.to_csv(output_file, index=False)
