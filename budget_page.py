import csv
from datetime import date, datetime
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tools import db_execute

LARGE_FONT = ("verdana", 16)


class BudgetPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # SETTING ELEMENTS
        self.parent = parent
        self.export = tk.Button(self, text='export to csv', command=BudgetPage.export_to_csv)
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
                                                                           item=self.exp_tree.item(
                                                                               self.exp_tree.focus())))
        self.exp_del_button = tk.Button(self,
                                        text="Delete expense",
                                        command=lambda: self.delete_window(
                                            item=self.exp_tree.item(self.exp_tree.focus())))

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
                                                                           item=self.inc_tree.item(
                                                                               self.inc_tree.focus())))
        self.inc_del_button = tk.Button(self,
                                        text="Delete income",
                                        command=lambda: self.delete_window(
                                            item=self.inc_tree.item(self.inc_tree.focus())))
        self.refresh_budget_page()

        # STYLING
        self.export.grid(row=0, column=0, sticky='w', padx=5, pady=5)
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

        self.balance_label['text'] = 'Current balance: {:.2f}'.format(BudgetPage.get_balance())

    @staticmethod
    def get_balance():
        budget = db_execute(
            sql='''SELECT IFNULL(SUM(CASE WHEN revenue_type='income' THEN amount ELSE 0 END) - 
                                 SUM(CASE WHEN revenue_type='expense' THEN amount ELSE 0 END), 0) AS balance
                           FROM revenues;''')
        return budget[0]['balance']

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
        window.date_value.insert(0, str(date.today()))
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
        window.name_value.insert(0, item['values'][1])
        window.amount_value.insert(0, item['values'][2])
        window.date_value.insert(0, item['values'][3])
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

    @staticmethod
    def export_to_csv():
        """
        Creates and saves csv file in selected by user directory, open file with default system application
        :return: None
        """
        # SHOWS ASK FOR DIRECTORY WINDOW
        file_dir = filedialog.asksaveasfilename(initialdir='/',
                                                title='Select file',
                                                filetypes=(('csv file', '*.csv'), ('all files', '*.*')))
        if not file_dir:
            return

        # CREATES FILE IN SELECTED DIRECTORY
        with open(file_dir, 'w', encoding='utf-8') as csv_file:

            field_names = ['name', 'revenue_type', 'amount', 'create_date']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

            # FINDS DATA STORED IN DB
            revenues = db_execute(sql='''SELECT name, revenue_type, amount, create_date FROM revenues;''')

            # SAVES DATA IN FILE
            for revenue in revenues:
                writer.writerow(revenue)
            writer.writerow({'name': '', 'revenue_type': 'SUM', 'amount': BudgetPage.get_balance(), 'create_date': ''})

        # OPENS SAVED FILE IN DEFAULT SYSTEM APPLICATION
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', file_dir))
        # FOR WINDOWS
        elif os.name == 'nt':
            os.startfile(file_dir)
            return
        # FOR UNIX
        elif os.name == 'posix':
            subprocess.call(('xdg-open', file_dir))


class AddUpdateElementWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.name_label = tk.Label(self, text='Name')
        self.name_value = tk.Entry(self)
        self.amount_label = tk.Label(self, text='Amount')
        self.amount_value = tk.Entry(self)
        self.date_label = tk.Label(self, text='Date')
        self.date_value = tk.Entry(self)
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.save = tk.Button(self, text='Save')

        self.name_label.grid(row=0, column=0, sticky='w', pady=5)
        self.name_value.grid(row=0, column=1, columnspan=2, sticky='e', padx=2)
        self.amount_label.grid(row=1, column=0, sticky='w', pady=5)
        self.amount_value.grid(row=1, column=1, columnspan=2, sticky='e', padx=2)
        self.date_label.grid(row=2, column=0, sticky='w', pady=5)
        self.date_value.grid(row=2, column=1, columnspan=2, sticky='e', padx=2)
        self.cancel.grid(row=3, column=1, pady=5, sticky='e')
        self.save.grid(row=3, column=2, pady=5, sticky='e')

    def add_revenue(self, revenue_type):
        """
        Adds new revenue to DB and refreshes trees elements
        :param revenue_type: (str) type of revenue (income, expense)
        :return: None
        """
        validated_data = self.validate_input()
        if validated_data:
            db_execute(sql='''INSERT INTO revenues VALUES (NULL, ?, ?, ?, ?);''',
                       variables=(validated_data[0],
                                  revenue_type,
                                  validated_data[1],
                                  validated_data[2]))
            self.parent.refresh_budget_page()
            self.destroy()

    def update_revenue(self, revenue_id):
        """
        Updates revenue selected by user and refreshes trees elements
        :param revenue_id: (int) ID of revenue stored in DB
        :return: None
        """
        validated_data = self.validate_input()
        if validated_data:
            db_execute(sql='''UPDATE revenues SET name=?, amount=?, create_date=? WHERE id=?;''',
                       variables=(validated_data[0],
                                  validated_data[1],
                                  validated_data[2],
                                  revenue_id))
            self.parent.refresh_budget_page()
            self.destroy()

    def validate_input(self):
        """
        Handles user input data validation. Raises tk.TopLevel widget frame as error if incorrect data is entered
        :return: tuple that stores correct data. None if data was incorrect.
        """
        # VALIDATES NAME ENTRY
        name = self.name_value.get()
        if name == '':
            ValidationError(self, text='Name can\'t be empty!', padx=10, pady=10)
            return
        # VALIDATES AMOUNT ENTRY
        try:
            amount = float(self.amount_value.get().replace(',', '.'))
        except ValueError:
            ValidationError(self, text='Amount must be a number!', padx=10, pady=10)
            return
        # VALIDATES DATE ENTRY
        try:
            create_date = datetime.strptime(self.date_value.get(), '%Y-%M-%d').date()
        except ValueError:
            ValidationError(self, text='Date should be in YYYY-MM-DD format!', padx=10, pady=10)
            return
        return name, amount, create_date


class ValidationError(tk.Toplevel):

    def __init__(self, parent, text, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.title('Error')
        self.msg = tk.Message(self, text=text, width=300)
        self.button = tk.Button(self, text="Dismiss", command=self.destroy)

        self.msg.grid(row=0, column=0, sticky='nsew', pady=5)
        self.button.grid(row=1, column=0, pady=5)


class DeleteElementWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.label = tk.Label(self, text='Are you sure you want to delete this element?')
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.delete = tk.Button(self, text='Delete')

        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=5)
        self.cancel.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.delete.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    def delete_revenue(self, revenue_id):
        """
        Deletes revenue from DB and refreshes trees elements
        :param revenue_id: (int) ID of revenue stored in DB
        :return: None
        """
        db_execute(
            sql='''DELETE FROM revenues WHERE id=?;''',
            variables=(revenue_id,))
        self.parent.refresh_budget_page()
        self.destroy()
