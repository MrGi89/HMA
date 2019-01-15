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

        back = tk.Button(self, text="< back", command=lambda: controller.show_frame(StartPage))
        balance_label = tk.Label(self, text='Current balance: {}'.format(self.budget), font=LARGE_FONT)
        expenses_tree = ttk.Treeview(self, columns=('Expenses', 'Amount'), show='headings')
        expenses_tree.heading('#1', text='Expenses')
        expenses_tree.heading('#2', text='Amount')
        expenses_tree.column('#1', stretch=tk.YES)
        expenses_tree.column('#2', stretch=tk.YES)
        # expenses_tree.insert('', 'end', text='', values=('Rent', '1200'))
        income_tree = ttk.Treeview(self, columns=('Incomes', 'Amount'), show='headings')
        income_tree.heading('#1', text='Incomes')
        income_tree.heading('#2', text='Amount')
        income_tree.column('#1', stretch=tk.YES)
        income_tree.column('#2', stretch=tk.YES)
        income_tree.insert('', 'end', text='', values=('Salary', '2200'))
        income_tree.insert('', 'end', text='', values=('Salary', '100'))
        income_tree.insert('', 'end', text='', values=('Salary', '1500'))

        add_exp_button = tk.Button(self, text="Add expense", command=lambda: self.add_expense())
        add_inc_button = tk.Button(self, text="Add income", command=lambda: self.add_balance('income'))
        upd_exp_button = tk.Button(self, text="Update expense", command=lambda: self.handle_balance('expense', expenses_tree.item(expenses_tree.focus())))
        upd_inc_button = tk.Button(self, text="Update income", command=lambda: self.handle_balance('income', income_tree.item(income_tree.focus())))
        del_exp_button = tk.Button(self, text="Delete expense")
        del_inc_button = tk.Button(self, text="Delete income")

        back.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        balance_label.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        expenses_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        income_tree.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        add_exp_button.grid(row=2, column=0, sticky='nsew', padx=5)
        add_inc_button.grid(row=2, column=1, sticky='nsew', padx=5)
        upd_exp_button.grid(row=3, column=0, sticky='nsew', padx=5)
        upd_inc_button.grid(row=3, column=1, sticky='nsew', padx=5)
        del_exp_button.grid(row=4, column=0, sticky='nsew', padx=5)
        del_inc_button.grid(row=4, column=1, sticky='nsew', padx=5)

    def add_expense(self):

        window = BalanceWindow(self, padx=20, pady=20)
        window.title = 'Add expense'

        title = window.title_entry.get()
        amount = window.amount_entry.get()
        date = window.date_entry.get()

        print(title, amount, date)


class BalanceWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.title = tk.Label(self, text='Title')
        self.title_entry = tk.Entry(self)
        self.amount = tk.Label(self, text='Amount')
        self.amount_entry = tk.Entry(self)
        self.date = tk.Label(self, text='Date')
        self.date_entry = tk.Entry(self)

        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.save = tk.Button(self, text='Save')

        self.title.grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky='e', padx=2)
        self.amount.grid(row=1, column=0, sticky='w', pady=5)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky='e', padx=2)
        self.date.grid(row=2, column=0, sticky='w', pady=5)
        self.date_entry.grid(row=2, column=1, columnspan=2, sticky='e', padx=2)
        self.cancel.grid(row=3, column=1, sticky='e')
        self.save.grid(row=3, column=2, sticky='e')

    def save(self):
        data = {'title': self.title_entry.get(),
                'amount': self.amount_entry.get(),
                'date': self.date_entry.get()}
        self.destroy()
        return data


if __name__ == "__main__":
    app = App()
    app.mainloop()
