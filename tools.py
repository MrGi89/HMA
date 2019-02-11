import sqlite3


def dict_factory(cursor, row):
    result = dict()
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def db_execute(sql, variables=tuple(), cursor_type='fetchall'):
    conn = sqlite3.connect('hma_db.sqlite')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(sql, variables)
    if cursor_type == 'fetchall':
        result = c.fetchall()
    elif cursor_type == 'fetchone':
        result = c.fetchone()
    else:
        result = c.lastrowid
    conn.commit()
    conn.close()
    return result
