import os
import glob
from preprocess import split_csv
from map import map_function
from shuffle import shuffle_data
from reduce import reduce_function
from sql_parser import parse_sql


def search(sql, input_folder, output_folder):
    input_folder = "./"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    parsed_sql = parse_sql(sql)
    # Map阶段 - 处理两个文件
    for csv_file in [parsed_sql['from'], parsed_sql['join']]:
        for chunk_file in os.listdir(input_folder):
            if chunk_file.startswith(f'chunk_{csv_file}_'):
                map_function(os.path.join(input_folder, chunk_file), csv_file.split('.')[0], parsed_sql, output_folder)

    # Shuffle阶段
    shuffle_data(os.path.join(output_folder, 'sorted_*.csv'), output_folder)

    # Reduce阶段 - 执行JOIN操作
    results = reduce_function(os.path.join(output_folder, 'shuffled_data.csv'), parsed_sql, output_folder, parsed_sql['from'], parsed_sql['join'])
    print(results)
    for file in glob.glob(output_folder + "/*"):  
        os.remove(file)  

def main():
    # 示例SQL语句
    # sql_query = "SELECT candle_begin_time, volume, symbol From BTC.csv WHERE volume < 1000 ORDER BY volume GROUP BY symbol MIN(volume)"
    # sql_query = "FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000 LINE volume BUNCH symbol min(volume)"

    # # sql_query = "SELECT candle_begin_time, volume, symbol From BTC.csv WHERE volume < 1000"
    # sql_query = "FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000"
    
    # # sql_query = "SELECT candle_begin_time, volume, symbol FROM BTC.csv WHERE volume < 1000 JOIN BTCALL.csv ON symbol"
    sql_query = "FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000 CONNECT BTCALL.csv ON symbol"
    
    csv_files = ['BTC.csv', 'BTCALL.csv']
    db_folder = 'data'
    chunk_size = 10000
    # 数据预处理 - 分割两个文件
    split_csv(csv_files[0], chunk_size, db_folder)
    split_csv(csv_files[1], chunk_size, db_folder)
    
    
    output_folder = 'output'
    search(sql_query, db_folder, output_folder)


if __name__ == "__main__":
    main()
