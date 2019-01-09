import tkinter as tk
from tkinter import ttk

from tools import db_execute


class App(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tree = None

        self.initialize_menu()
        self.initialize_ui()

    def initialize_menu(self):
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        file = tk.Menu(menu)
        options = tk.Menu(menu)
        about = tk.Menu(menu)

        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Options", menu=options)
        menu.add_cascade(label="About", menu=about)

        file.add_command(label="Import from...", command=self.parent.quit)
        file.add_command(label="Export to...", command=self.parent.quit)
        file.add_command(label="Exit", command=self.parent.quit)

    def initialize_ui(self):
        self.parent.title('Home budget')
        self.parent.geometry('800x600')

        balance = self.get_balance()
        tk.Label(text=str(balance)).grid(row=1, column=0, sticky=tk.E)
        tk.Entry().grid(row=1, column=1, sticky=tk.E)

        self.tree = ttk.Treeview(self.parent, columns=('Wydatki', 'Kwota', 'Wpływy'))
        self.tree.heading('#0', text='Wydatki')
        self.tree.heading('#1', text='Kwota')
        self.tree.heading('#2', text='Wpływy')
        self.tree.heading('#3', text='Kwota')
        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', width=80, stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)
        self.tree.column('#3', width=80, stretch=tk.YES)
        self.tree.grid(row=4, columnspan=3, sticky=tk.NSEW)
        self.insert_to_tree()

    def insert_to_tree(self):
        # self.tree.insert('', 'end', 1, text='Karta miejska')
        pass

    def get_balance(self):
        return 'balance'


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.mainloop()
