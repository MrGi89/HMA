import tkinter as tk
from tkinter import ttk


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = dict()
        frame = StartPage(container, self)
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames = {'start_page': frame}
        self.show_frame('start_page')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Start Page').pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()

# class App(tk.Frame):
#
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         self.parent = parent
#         self.expenses_tree = None
#         self.income_tree = None
#
#         self.initialize_menu()
#         self.initialize_ui()
#
#     def initialize_menu(self):
#         menu = tk.Menu(self.parent)
#         self.parent.config(menu=menu)
#
#         file = tk.Menu(menu)
#         options = tk.Menu(menu)
#         about = tk.Menu(menu)
#
#         menu.add_cascade(label="File", menu=file)
#         menu.add_cascade(label="Options", menu=options)
#         menu.add_cascade(label="About", menu=about)
#
#         file.add_command(label="Import from...", command=self.parent.quit)
#         file.add_command(label="Export to...", command=self.parent.quit)
#         file.add_command(label="Exit", command=self.parent.quit)
#
#     def initialize_ui(self):
#         self.parent.title('Home budget')
#         self.parent.geometry('800x600')
#
#         tk.Frame(height=20, bd=1, relief=tk.SUNKEN).grid(row=0, column=0, columnspan=3)
#
#         tk.Label(text='First Name').grid(row=1, column=0, sticky=tk.W)
#         tk.Entry().grid(row=1, column=1, sticky=tk.E)
#         tk.Label(text='Last Name').grid(row=2, column=0, sticky=tk.W)
#         tk.Entry().grid(row=2, column=1, sticky=tk.E)
#         tk.Label(text='Balance').grid(row=3, column=0, sticky=tk.W)
#         tk.Label(text=str(self.get_balance())).grid(row=3, column=1, sticky=tk.E)
#
#         tk.Frame(height=10, width=100).grid(row=2, column=2, rowspan=2)
#
#         tk.Button(self.parent, text="Save changes", command=self.parent.quit, width=50).grid(row=1, column=3, sticky=tk.W)
#         tk.Button(self.parent, text="Add expense", command=self.parent.quit, width=50).grid(row=2, column=3, sticky=tk.W)
#         tk.Button(self.parent, text="Add income", command=self.parent.quit, width=50).grid(row=3, column=3, sticky=tk.W)
#
#         tk.Frame(height=20, bd=1, relief=tk.SUNKEN).grid(row=4, column=0, columnspan=3)
#
#         self.expenses_tree = ttk.Treeview(self.parent, columns=('Expenses', 'Amount'), show='headings')
#         self.expenses_tree.heading('#1', text='Expenses')
#         self.expenses_tree.heading('#2', text='Amount')
#         self.expenses_tree.column('#1', stretch=tk.YES)
#         self.expenses_tree.column('#2', width=80, stretch=tk.YES)
#         self.expenses_tree.grid(row=5, column=0, columnspan=2, sticky=tk.W)
#         self.expenses_tree.insert('', 'end', text='', values=('Widget Tour', '22'))
#
#         tk.Frame(height=10, width=100).grid(row=5, column=2)
#
#         self.income_tree = ttk.Treeview(self.parent, columns=('Income', 'Amount'), show='headings')
#         self.income_tree.heading('#1', text='Income')
#         self.income_tree.heading('#2', text='Amount')
#         self.income_tree.column('#1', stretch=tk.YES)
#         self.income_tree.column('#2', width=80, stretch=tk.YES)
#         self.income_tree.grid(row=5, column=3, columnspan=2, sticky=tk.W)
#         self.income_tree.insert('', 'end', text='', values=('Salary', '2200'))
#
#     def insert_to_tree(self):
#         # self.tree.insert('', 'end', 1, text='Karta miejska')
#         pass
#
#     def get_balance(self):
#         return 22.5
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     app.mainloop()
