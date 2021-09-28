import json
import mariadb

db_pool = mariadb.ConnectionPool(
    pool_name="metisai_mariadb_connection_pool",
    pool_size=5,
    pool_reset_connection=False,
    host="db.metis-ai.com",
    user="metisai",
    password="metisai",
    database="MetisAI",
)


def exec_select_stmt(sql_stmt):
    conn, curs = None, None
    try:
        conn = db_pool.get_connection()
        curs = conn.cursor()
        # curs.execute(f"USE {db_name}")
        curs.execute(sql_stmt)
        col_names = [col_desp[0] for col_desp in curs.description]
        # print(f"Affects {curs.fieldcount()} {col_names} rows.")
        rlts = curs.fetchall()
        row_data_dicts = []
        for rlt in rlts:
            # print(rlt)
            row_data_dict = {}
            for kv in zip(col_names, rlt):
                row_data_dict[kv[0]] = kv[1]
            row_data_dicts.append(row_data_dict)
        return json.dumps(row_data_dicts)
    except mariadb.Error as e:
        print(f"Error: {e}")
    finally:
        if curs:
            curs.close()
        if conn:
            conn.close()
    return
    # return '[{"State": "Colorado", "County": "Denver"}, {"State": "Colorado", "County": "Arapahoe/Adams"}, {"State": "Colorado", "County": "Garfield"}, {"State": "Colorado", "County": "Jefferson"}, {"State": "Colorado", "County": "Jefferson"}, {"State": "Colorado", "County": "Douglas County"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Weid"}, {"State": "Colorado", "County": "Pueblo"}, {"State": "Colorado", "County": "Pueblo"}, {"State": "Colorado", "County": "Mesa"}, {"State": "Colorado", "County": "Kiowa"}, {"State": "Colorado", "County": "El Paso"}, {"State": "Colorado", "County": "Baca"}, {"State": "Colorado", "County": "Denver"}, {"State": "Colorado", "County": "Denver"}, {"State": "Colorado", "County": "Logan"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Mesa"}, {"State": "Colorado", "County": "Cleer Creek"}, {"State": "Colorado", "County": "Pueblo"}, {"State": "Colorado", "County": "El Paso"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Arapahoe"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Adams/Jefferson"}, {"State": "Colorado", "County": "Adams"}, {"State": "Colorado", "County": "Pueblo"}, {"State": "Colorado", "County": "La Plata"}, {"State": "Colorado", "County": "El Paso"}, {"State": "Colorado", "County": "Mesa"}]'
