import sqlite3
import tkinter as tk
CURRENT_USER = {'id': None, 'username': None}


class ValidationError(tk.Toplevel):

    def __init__(self, parent, text, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.title('Error')
        self.msg = tk.Message(self, text=text, width=300)
        self.button = tk.Button(self, text="Dismiss", command=self.destroy)
        self.msg.grid(row=0, column=0, sticky='nsew', pady=5)
        self.button.grid(row=1, column=0, pady=5)


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
