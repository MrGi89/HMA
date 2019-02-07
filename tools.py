import sqlite3


def dict_factory(cursor, row):
    result = dict()
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def db_execute(sql, variables=tuple()):

    conn = sqlite3.connect('budget.sqlite')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(sql, variables)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result
