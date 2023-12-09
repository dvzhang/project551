import pandas as pd
import os
from collections import defaultdict

def custom_join(table_A, table_B, join_column):
    table_B_dict = defaultdict(list)
    for _, row in table_B.iterrows():
        table_B_dict[row[join_column]].append(row)

    joined_data = []
    for _, row_A in table_A.iterrows():
        if row_A[join_column] in table_B_dict:
            for row_B in table_B_dict[row_A[join_column]]:
                # 为每个表中的属性添加后缀
                joined_row = {f'{col}_a': value for col, value in row_A.items()}
                joined_row.update({f'{col}_b': value for col, value in row_B.items() if col != join_column})
                joined_data.append(joined_row)

    return pd.DataFrame(joined_data)


def custom_groupby(data, group_by_column, agg_functions):
    grouped_data = defaultdict(lambda: defaultdict(list))
    # 将数据分组
    for _, row in data.iterrows():
        key = row[group_by_column]
        for col in data.columns:
            grouped_data[key][col].append(row[col])

    # 应用聚合函数
    result = []
    for key, values in grouped_data.items():
        aggregated_row = {group_by_column: key}
        for col, vals in values.items():
            if col in agg_functions:
                if 'count' in agg_functions[col]:
                    aggregated_row[f'count_{col}'] = len(vals)
                if 'sum' in agg_functions[col]:
                    aggregated_row[f'sum_{col}'] = sum(vals)
                if 'avg' in agg_functions[col]:
                    aggregated_row[f'avg_{col}'] = sum(vals) / len(vals) if vals else 0
                if 'max' in agg_functions[col]:
                    aggregated_row[f'max_{col}'] = max(vals)
                if 'min' in agg_functions[col]:
                    aggregated_row[f'min_{col}'] = min(vals)
        result.append(aggregated_row)
    return pd.DataFrame(result)


def reduce_function(input_file, parsed_sql, output_folder, source_table = "", join_table = ""):
    source_table = source_table.split(".")[0]
    if join_table: 
        join_table = join_table.split(".")[0] 
    
    data = pd.read_csv(input_file, parse_dates=['candle_begin_time'])
    
    if parsed_sql.get('join'):
        table_A = data[data['source_table'] == source_table]
        table_B = data[data['source_table'] == join_table]
        joined_data = custom_join(table_A, table_B, parsed_sql['on'])
        if parsed_sql.get('group_by'):
            result = custom_groupby(joined_data, parsed_sql['group_by'], parsed_sql['agg_functions'])
        else:
            result = joined_data
    elif parsed_sql.get('group_by'):
        result = custom_groupby(data, parsed_sql['group_by'], parsed_sql['agg_functions'])
    else:
        result = data

    result.to_csv(os.path.join(output_folder, 'joined_data.csv'), index=False)
    return result