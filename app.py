from datetime import date
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
        tk.Button(self, text="Budget", height=2, font=MEDIUM_FONT,
                  command=lambda: controller.show_frame(BudgetPage)).pack(fill='both', pady=5)
        tk.Button(self, text="Shopping list", height=2, font=MEDIUM_FONT).pack(fill='both', pady=5)
        tk.Button(self, text="Cook book", height=2, font=MEDIUM_FONT).pack(fill='both', pady=5)
        tk.Button(self, text="Exit", height=2, font=MEDIUM_FONT, command=quit).pack(fill='both', pady=5)


class BudgetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.budget = 2000

        back = tk.Button(self, text="< back", command=lambda: controller.show_frame(StartPage))
        balance_label = tk.Label(self, text='Current balance: {}'.format(self.budget), font=LARGE_FONT)
        exp_tree = ttk.Treeview(self, columns=('Expenses', 'Amount', 'Date'), show='headings')
        exp_tree.heading('#1', text='Expenses', anchor=tk.CENTER)
        exp_tree.heading('#2', text='Amount', anchor=tk.CENTER)
        exp_tree.heading('#3', text='Date', anchor=tk.CENTER)
        exp_tree.column('#1', width=200, stretch=tk.NO)
        exp_tree.column('#2', width=100, stretch=tk.NO, anchor=tk.CENTER)
        exp_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.CENTER)
        exp_tree.bind('<Button-1>', self.activate_exp_button)

        inc_tree = ttk.Treeview(self, columns=('Incomes', 'Amount', 'Date'), show='headings')
        inc_tree.heading('#1', text='Incomes', anchor=tk.CENTER)
        inc_tree.heading('#2', text='Amount', anchor=tk.CENTER)
        inc_tree.heading('#3', text='Date', anchor=tk.CENTER)
        inc_tree.column('#1', width=200, stretch=tk.NO)
        inc_tree.column('#2', width=100, stretch=tk.NO, anchor=tk.CENTER)
        inc_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.CENTER)
        inc_tree.bind('<Button-1>', self.activate_inc_button)

        exp_tree.insert('', 'end', text='', values=('Rent', '1200', '2019-01-01'))
        exp_tree.insert('', 'end', text='', values=('Rent2', '2200', '2019-01-02'))
        exp_tree.insert('', 'end', text='', values=('Rent3', '200', '2019-01-03'))
        inc_tree.insert('', 'end', text='', values=('Salary', '2200', '2019-01-04'))
        inc_tree.insert('', 'end', text='', values=('Salary2', '100', '2019-01-05'))
        inc_tree.insert('', 'end', text='', values=('Salary3', '1500', '2019-01-06'))

        exp_add_button = tk.Button(self, text="Add expense", command=lambda: self.add_position('exp'))
        self.exp_upd_button = tk.Button(self, text="Update expense", state='disabled',
                                        command=lambda: self.update_position('exp', exp_tree.item(exp_tree.focus())))
        self.exp_del_button = tk.Button(self, text="Delete expense", state='disabled',
                                        command=lambda: self.update_position('exp', exp_tree.item(exp_tree.focus())))

        inc_add_button = tk.Button(self, text="Add income", command=lambda: self.add_position('inc'))
        self.inc_upd_button = tk.Button(self, text="Update income", state='disabled',
                                        command=lambda: self.update_position('inc', inc_tree.item(inc_tree.focus())))
        self.inc_del_button = tk.Button(self, text="Delete income", state='disabled',
                                        command=lambda: self.delete_position('inc', inc_tree.item(inc_tree.focus())))

        back.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        balance_label.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        exp_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        inc_tree.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        exp_add_button.grid(row=2, column=0, sticky='nsew', padx=5)
        self.exp_upd_button.grid(row=3, column=0, sticky='nsew', padx=5)
        self.exp_del_button.grid(row=4, column=0, sticky='nsew', padx=5)
        inc_add_button.grid(row=2, column=1, sticky='nsew', padx=5)
        self.inc_upd_button.grid(row=3, column=1, sticky='nsew', padx=5)
        self.inc_del_button.grid(row=4, column=1, sticky='nsew', padx=5)

    def activate_exp_button(self, event):

        self.exp_upd_button.configure(state='normal')
        self.exp_del_button.configure(state='normal')

    def activate_inc_button(self, event):

        self.inc_upd_button.configure(state='normal')
        self.inc_del_button.configure(state='normal')

    def add_position(self, table):

        window = AddUpdateBalanceWindow(self, padx=10, pady=10)
        window.date_entry.insert(0, str(date.today()))

        if table == 'exp':
            window.title('Add expense')
            window.save['command'] = window.add_expense
        else:
            window.title('Add income')
            window.save['command'] = window.add_income

    def update_position(self, table, item):

        if not item['values']:
            alert = tk.Toplevel(padx=10, pady=10)
            alert.title('Something went wrong!')
            alert_text = 'If you wan\'t to delete or update one of existing items\n please select it and then click the wright button'
            tk.Label(alert, text=alert_text).pack(fill='both', pady=5)
            tk.Button(alert, text='Dismiss', command=alert.destroy).pack(pady=5)
            return
        window = AddUpdateBalanceWindow(self, padx=20, pady=20)
        window.name_entry.insert(0, item['values'][0])
        window.amount_entry.insert(0, item['values'][1])
        window.date_entry.insert(0, item['values'][2])

        if table == 'exp':
            window.title('Update expense')
            window.save['command'] = window.update_expense
        else:
            window.title('Update income')
            window.save['command'] = window.update_income

    def delete_position(self, table, item):
        pass
        # window = DeleteBalanceWindow(self, padx=10, pady=10)
        #
        # if table == 'exp':
        #     window.title(Delete expense')
        #     window.save['command'] = window.delete_expense
        # else:
        #     window.title('Delete income')
        #     window.save['command'] = window.delete_income


class AddUpdateBalanceWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.name = tk.Label(self, text='Name')
        self.name_entry = tk.Entry(self)
        self.amount = tk.Label(self, text='Amount')
        self.amount_entry = tk.Entry(self)
        self.date = tk.Label(self, text='Date')
        self.date_entry = tk.Entry(self)
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.save = tk.Button(self, text='Save')

        self.name.grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky='e', padx=2)
        self.amount.grid(row=1, column=0, sticky='w', pady=5)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky='e', padx=2)
        self.date.grid(row=2, column=0, sticky='w', pady=5)
        self.date_entry.grid(row=2, column=1, columnspan=2, sticky='e', padx=2)
        self.cancel.grid(row=3, column=1, pady=5, sticky='e')
        self.save.grid(row=3, column=2, pady=5, sticky='e')

    def add_expense(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

    def update_expense(self):
        pass

    def delete_expense(self):
        pass

    def add_income(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

    def update_income(self):
        pass

    def delete_income(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
