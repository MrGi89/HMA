import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("verdana", 16)
MEDIUM_FONT = ("verdana", 12)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Home Management Application')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.init_menu(container)

        self.frames = dict()
        for item in (StartPage, BudgetPage):
            frame = item(container, self)
            frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
            self.frames[item] = frame
        self.show_frame(StartPage)

    def init_menu(self, container):
        menu_bar = tk.Menu(container)
        file = tk.Menu(menu_bar, tearoff=0)
        options = tk.Menu(menu_bar, tearoff=0)
        about = tk.Menu(menu_bar, tearoff=0)

        file.add_command(label="Main menu", command=lambda: self.show_frame(StartPage))
        file.add_separator()
        file.add_command(label="Import from...", command=quit)
        file.add_command(label="Export to...", command=quit)
        file.add_separator()
        file.add_command(label="Exit", command=quit)

        menu_bar.add_cascade(label="File", menu=file)
        menu_bar.add_cascade(label="Options", menu=options)
        menu_bar.add_cascade(label="About", menu=about)

        tk.Tk.config(self, menu=menu_bar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        welcome_text = '''Welcome to Home Management Application!!!\nChoose what you wan\'t to do from options below:'''
        tk.Label(self, text=welcome_text, font=LARGE_FONT).pack(pady=30)
        tk.Button(self, text="Budget", height=2, font=MEDIUM_FONT, command=lambda: controller.show_frame(BudgetPage)).pack(fill='both', pady=5)
        tk.Button(self, text="Shopping list", height=2, font=MEDIUM_FONT).pack(fill='both', pady=5)
        tk.Button(self, text="Cook book", height=2, font=MEDIUM_FONT).pack(fill='both', pady=5)
        tk.Button(self, text="Exit", height=2, font=MEDIUM_FONT, command=quit).pack(fill='both', pady=5)


class BudgetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.budget = 2000

        tk.Button(self, text="< back", command=lambda: controller.show_frame(StartPage)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        tk.Label(self, text='Current balance: {}'.format(self.budget), font=LARGE_FONT).grid(row=0, column=1, sticky='e', padx=5, pady=5)

        expenses_tree = ttk.Treeview(self, columns=('Expenses', 'Amount'), show='headings')
        expenses_tree.heading('#1', text='Expenses')
        expenses_tree.heading('#2', text='Amount')
        expenses_tree.column('#1', stretch=tk.YES)
        expenses_tree.column('#2', stretch=tk.YES)
        expenses_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        expenses_tree.insert('', 'end', text='', values=('Rent', '1200'))

        income_tree = ttk.Treeview(self, columns=('Incomes', 'Amount'), show='headings')
        income_tree.heading('#1', text='Incomes')
        income_tree.heading('#2', text='Amount')
        income_tree.column('#1', stretch=tk.YES)
        income_tree.column('#2', stretch=tk.YES)
        income_tree.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        income_tree.insert('', 'end', text='', values=('Salary', '2200'))

        tk.Button(self, text="Add expense", command=self.add_expense).grid(row=2, column=0, sticky='nsew', padx=5)
        tk.Button(self, text="Add income").grid(row=2, column=1, sticky='nsew', padx=5)
        tk.Button(self, text="Update expense").grid(row=3, column=0, sticky='nsew', padx=5)
        tk.Button(self, text="Update income").grid(row=3, column=1, sticky='nsew', padx=5)
        tk.Button(self, text="Delete expense").grid(row=4, column=0, sticky='nsew', padx=5)
        tk.Button(self, text="Delete income").grid(row=4, column=1, sticky='nsew', padx=5)

    def add_expense(self):

        top = tk.Toplevel(self, padx=20, pady=20)
        top.title("Add expense")

        tk.Label(top, text='Title').grid(row=0, column=0, sticky='w', pady=5)
        tk.Entry(top).grid(row=0, column=1, columnspan=2, sticky='e', padx=2)

        tk.Label(top, text='Amount').grid(row=1, column=0, sticky='w', pady=5)
        tk.Entry(top).grid(row=1, column=1, columnspan=2, sticky='e', padx=2)

        tk.Label(top, text='Date').grid(row=2, column=0, sticky='w', pady=5)
        tk.Entry(top).grid(row=2, column=1, columnspan=2, sticky='e', padx=2)

        tk.Button(top, text='Cancel', command=top.destroy).grid(row=4, column=1, sticky='e')
        tk.Button(top, text='Add').grid(row=4, column=2, sticky='e')


if __name__ == "__main__":
    app = App()
    app.mainloop()

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

