import sqlite3


def db_execute(sql, variables=tuple()):

    conn = sqlite3.connect('budget.sqlite')
    c = conn.cursor()
    c.execute(sql, variables)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result
