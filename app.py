from datetime import date
import tkinter as tk
from tkinter import ttk
from tools import db_execute

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
            frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
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
        tk.Label(self, text=welcome_text, font=MEDIUM_FONT).pack(pady=70)
        tk.Button(self, text="Budget", height=1, font=MEDIUM_FONT,
                  command=lambda: controller.show_frame(BudgetPage)).pack(fill='both', pady=5)
        tk.Button(self, text="Shopping list", height=1, font=MEDIUM_FONT, state='disabled').pack(fill='both', pady=5)
        tk.Button(self, text="Cook book", height=1, font=MEDIUM_FONT, state='disabled').pack(fill='both', pady=5)
        tk.Button(self, text="Exit", height=1, font=MEDIUM_FONT, command=quit).pack(fill='both', pady=5)


class BudgetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # SETTING ELEMENTS

        self.parent = parent
        self.back = tk.Button(self, text="menu", command=lambda: controller.show_frame(StartPage))
        self.balance_label = tk.Label(self, font=LARGE_FONT)
        self.exp_tree = ttk.Treeview(self, columns=('id', 'Expense', 'Amount', 'Date'), show='headings',
                                     selectmode='browse')
        self.exp_tree.heading('#2', text='Expense', anchor=tk.CENTER)
        self.exp_tree.heading('#3', text='Amount', anchor=tk.CENTER)
        self.exp_tree.heading('#4', text='Date', anchor=tk.CENTER)
        self.exp_tree.column('#2', width=150, stretch=tk.NO)
        self.exp_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.E)
        self.exp_tree.column('#4', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.exp_tree["displaycolumns"] = ('Expense', 'Amount', 'Date')
        self.exp_tree.bind('<ButtonRelease-1>', self.activate_exp_button)
        self.exp_add_button = tk.Button(self,
                                        text="Add expense",
                                        command=lambda: self.add_window(title='Add expense', revenue_type='expense'))
        self.exp_upd_button = tk.Button(self,
                                        text="Update expense",
                                        command=lambda: self.update_window(title='Update expense',
                                                                           item=self.exp_tree.item(self.exp_tree.focus())))
        self.exp_del_button = tk.Button(self,
                                        text="Delete expense",
                                        command=lambda: self.delete_window(item=self.exp_tree.item(self.exp_tree.focus())))

        self.inc_tree = ttk.Treeview(self, columns=('id', 'Income', 'Amount', 'Date'), show='headings',
                                     selectmode='browse')
        self.inc_tree.heading('#2', text='Income', anchor=tk.CENTER)
        self.inc_tree.heading('#3', text='Amount', anchor=tk.CENTER)
        self.inc_tree.heading('#4', text='Date', anchor=tk.CENTER)
        self.inc_tree.column('#2', width=150, stretch=tk.NO)
        self.inc_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.E)
        self.inc_tree.column('#4', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.inc_tree["displaycolumns"] = ('Income', 'Amount', 'Date')
        self.inc_tree.bind('<ButtonRelease-1>', self.activate_inc_button)
        self.inc_add_button = tk.Button(self,
                                        text="Add income",
                                        command=lambda: self.add_window(title='Add income', revenue_type='income'))
        self.inc_upd_button = tk.Button(self,
                                        text="Update income",
                                        command=lambda: self.update_window(title='Update income',
                                                                           item=self.inc_tree.item(self.inc_tree.focus())))
        self.inc_del_button = tk.Button(self,
                                        text="Delete income",
                                        command=lambda: self.delete_window(item=self.inc_tree.item(self.inc_tree.focus())))
        self.refresh_budget_page()

        # STYLING

        self.back.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.balance_label.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        self.exp_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.inc_tree.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.exp_add_button.grid(row=2, column=0, sticky='nsew', padx=5)
        self.exp_upd_button.grid(row=3, column=0, sticky='nsew', padx=5)
        self.exp_del_button.grid(row=4, column=0, sticky='nsew', padx=5)
        self.inc_add_button.grid(row=2, column=1, sticky='nsew', padx=5)
        self.inc_upd_button.grid(row=3, column=1, sticky='nsew', padx=5)
        self.inc_del_button.grid(row=4, column=1, sticky='nsew', padx=5)

    def refresh_budget_page(self):
        """
        Refreshes budget page data, deactivates buttons, inserts correct values to trees and sets actual balance
        :return: None
        """
        # CLEARS TREE
        self.exp_tree.delete(*self.exp_tree.get_children())
        self.inc_tree.delete(*self.inc_tree.get_children())
        self.deactivate_buttons()
        # RETRIEVES AND ADDS ACTUAL ELEMENTS TO TREES
        revenues = db_execute(sql='''SELECT * FROM revenues ORDER BY create_date DESC, amount DESC;''')
        for revenue in revenues:
            if revenue['revenue_type'] == 'expense':
                self.exp_tree.insert('', 'end', values=(revenue['id'],
                                                        revenue['name'],
                                                        '{:.2f}'.format(revenue['amount']),
                                                        revenue['create_date']))
            else:
                self.inc_tree.insert('', 'end', values=(revenue['id'],
                                                        revenue['name'],
                                                        '{:.2f}'.format(revenue['amount']),
                                                        revenue['create_date']))
        # SETS ACTUAL BALANCE
        budget = db_execute(
            sql='''SELECT ROUND(SUM(CASE WHEN revenue_type='income' THEN amount ELSE 0 END) - 
                          SUM(CASE WHEN revenue_type='expense' THEN amount ELSE 0 END), 2) AS balance
                   FROM revenues;''')
        self.balance_label['text'] = 'Current balance: {:.2f}'.format(budget[0]['balance'])

    def activate_exp_button(self, event):
        """
        Event handler that enables usage of update and delete buttons only after selecting one of expenses tree element
        :param event: not used
        :return: None
        """
        if self.exp_tree.focus() == '':
            return
        self.exp_upd_button.configure(state='normal')
        self.exp_del_button.configure(state='normal')

    def activate_inc_button(self, event):
        """
        Event handler that enables usage of update and delete buttons only after selecting one of incomes tree element
        :param event: not used
        :return: None
        """
        if self.inc_tree.focus() == '':
            return
        self.inc_upd_button.configure(state='normal')
        self.inc_del_button.configure(state='normal')

    def deactivate_buttons(self):
        """
        Function used to deactivate update and delete buttons after deleting or updating trees elements
        :return: None
        """
        self.exp_upd_button.configure(state='disabled')
        self.exp_del_button.configure(state='disabled')
        self.inc_upd_button.configure(state='disabled')
        self.inc_del_button.configure(state='disabled')

    def add_window(self, title, revenue_type):
        """
        Handles configuration of window used to add new tree element
        :param title: (str) used to configure window title
        :param revenue_type: (str) type of revenue (income, expense)
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=10, pady=10)
        window.title(title)
        window.title()
        window.title('Add income')
        window.date_entry.insert(0, str(date.today()))
        window.save['command'] = lambda: window.add_revenue(revenue_type)

    def update_window(self, title, item):
        """
        Handles configuration of window used to update trees element
        :param title: (str) used to configure window title
        :param item: (dict) stores selected item values
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=20, pady=20)
        window.title(title)
        window.name_entry.insert(0, item['values'][1])
        window.amount_entry.insert(0, item['values'][2])
        window.date_entry.insert(0, item['values'][3])
        window.save['command'] = lambda: window.update_revenue(revenue_id=item['values'][0])

    def delete_window(self, item):
        """
        Handles configuration of window used to delete tree element
        :param item: (dict) stores selected item values
        :return: None
        """
        window = DeleteElementWindow(self, padx=10, pady=10)
        window.title('Delete element?')
        window.delete['command'] = lambda: window.delete_revenue(revenue_id=item['values'][0])


class AddUpdateElementWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
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

    def add_revenue(self, revenue_type):
        """
        Adds new revenue to DB and refreshes trees elements
        :param revenue_type: (str) type of revenue (income, expense)
        :return: None
        """
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        exp_date = self.date_entry.get()
        db_execute(sql='''INSERT INTO revenues VALUES (NULL, ?, ?, ?, ?);''',
                   variables=(name, revenue_type, amount, exp_date))
        self.parent.refresh_budget_page()
        self.destroy()

    def update_revenue(self, revenue_id):
        """
        Updates revenue selected by user and refreshes trees elements
        :param revenue_id: (int) ID of revenue stored in DB
        :return: None
        """
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        exp_date = self.date_entry.get()
        db_execute(sql='''UPDATE revenues SET name=?, amount=?, create_date=? WHERE id=?;''',
                   variables=(name, amount, exp_date, revenue_id))
        self.parent.refresh_budget_page()
        self.destroy()


class DeleteElementWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.label = tk.Label(self, text='Are you sure you want to delete this element?')
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.delete = tk.Button(self, text='Delete')

        self.label.grid(row=0, column=0, sticky='nsew', pady=5)
        self.cancel.grid(row=1, column=0, pady=5, sticky='e')
        self.delete.grid(row=1, column=1, pady=5, sticky='e')

    def delete_revenue(self, revenue_id):
        """
        Deletes revenue from DB and refreshes trees elements
        :param revenue_id: (int) ID of revenue stored in DB
        :return: None
        """
        db_execute(
            sql='''DELETE FROM revenues WHERE id=?;''',
            variables=(revenue_id, ))
        self.parent.refresh_budget_page()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
