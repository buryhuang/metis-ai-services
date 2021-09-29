# import json
# import mariadb

# db_pool = mariadb.ConnectionPool(
#     pool_name="metisai_mariadb_connection_pool",
#     pool_size=5,
#     pool_reset_connection=False,
#     host="db.metis-ai.com",
#     user="metisai",
#     password="metisai",
#     database="MetisAI",
# )


# def exec_select_stmt(sql_stmt):
#     conn, curs = None, None
#     try:
#         conn = db_pool.get_connection()
#         curs = conn.cursor()
#         curs.execute(sql_stmt)
#         col_names = [col_desp[0] for col_desp in curs.description]
#         # print(f"Affects {curs.fieldcount()} {col_names} rows.")
#         rlts = curs.fetchall()
#         row_data_dicts = []
#         for rlt in rlts:
#             row_data_dict = {}
#             for kv in zip(col_names, rlt):
#                 row_data_dict[kv[0]] = kv[1]
#             row_data_dicts.append(row_data_dict)
#         return json.dumps(row_data_dicts)
#     except mariadb.Error as e:
#         print(f"Error: {e}")
#     finally:
#         if curs:
#             curs.close()
#         if conn:
#             conn.close()
#     return
#     # return '[{"State": "Colorado", "County": "Denver"}]'
