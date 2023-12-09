import re

def parse_sql(sql):
    sql_components = {
        "select": [],
        "from": None,
        "where": None,
        "order_by": None,
        "group_by": None,
        "agg_functions": {},
        "join": None,
        "on": None
    }

    # 修改正则表达式以匹配新的关键字
    from_match = re.search(r"FROM (.+?)( FIND| LINE| BUNCH| CONNECT|$)", sql, re.IGNORECASE)
    if from_match:
        sql_components["from"] = from_match.group(1).strip()

    select_match = re.search(r"FIND (.+?) CHARACTER", sql, re.IGNORECASE)
    if select_match:
        sql_components["select"] = select_match.group(1).split(" ")
        # sql_components["select"] = select_match.group(1).replace(' ', '').split(",")

    where_match = re.search(r"CHARACTER (.+?)( LINE| BUNCH| CONNECT|$)", sql, re.IGNORECASE)
    if where_match:
        sql_components["where"] = where_match.group(1).strip()

    order_by_match = re.search(r"LINE (.+?)( BUNCH| CONNECT|$)", sql, re.IGNORECASE)
    if order_by_match:
        sql_components["order_by"] = order_by_match.group(1).strip()

    group_by_match = re.search(r"BUNCH (.+?)( count|min|max|avg|sum|CONNECT|$)", sql, re.IGNORECASE)
    if group_by_match:
        sql_components["group_by"] = group_by_match.group(1).strip()

    agg_funcs_match = re.findall(r"(count|min|max|avg|sum)\((.+?)\)", sql, re.IGNORECASE)
    for func, column in agg_funcs_match:
        if column.strip() not in sql_components["agg_functions"]:
            sql_components["agg_functions"][column.strip()] = []
        sql_components["agg_functions"][column.strip()].append(func.lower())

    join_match = re.search(r"CONNECT (.+?) ON (.+)", sql, re.IGNORECASE)
    if join_match:
        sql_components["join"] = join_match.group(1).strip()
        sql_components["on"] = join_match.group(2).strip()

    return sql_components





# import re

# def parse_sql(sql):
#     sql_components = {
#         "select": [],
#         "from": None,
#         "where": None,
#         "order_by": None,
#         "group_by": None,
#         "agg_functions": {},
#         "join": None,
#         "on": None
#     }

#     select_match = re.search(r"SELECT (.+?) FROM", sql, re.IGNORECASE)
#     if select_match:
#         sql_components["select"] = select_match.group(1).replace(' ', '').split(",")

#     from_match = re.search(r"FROM (.+?)( WHERE| ORDER BY| GROUP BY| JOIN|$)", sql, re.IGNORECASE)
#     if from_match:
#         sql_components["from"] = from_match.group(1).strip()

#     where_match = re.search(r"WHERE (.+?)( ORDER BY| GROUP BY| JOIN|$)", sql, re.IGNORECASE)
#     if where_match:
#         sql_components["where"] = where_match.group(1).strip()

#     order_by_match = re.search(r"ORDER BY (.+?)( GROUP BY| JOIN|$)", sql, re.IGNORECASE)
#     if order_by_match:
#         sql_components["order_by"] = order_by_match.group(1).strip()

#     group_by_match = re.search(r"GROUP BY (.+?)( count|min|max|avg|sum|JOIN|$)", sql, re.IGNORECASE)
#     if group_by_match:
#         sql_components["group_by"] = group_by_match.group(1).strip()

#     agg_funcs_match = re.findall(r"(count|min|max|avg|sum)\((.+?)\)", sql, re.IGNORECASE)
#     for func, column in agg_funcs_match:
#         if column.strip() not in sql_components["agg_functions"]:
#             sql_components["agg_functions"][column.strip()] = []
#         sql_components["agg_functions"][column.strip()].append(func.lower())

#     join_match = re.search(r"JOIN (.+?) ON (.+)", sql, re.IGNORECASE)
#     if join_match:
#         sql_components["join"] = join_match.group(1).strip()
#         sql_components["on"] = join_match.group(2).strip()

#     return sql_components