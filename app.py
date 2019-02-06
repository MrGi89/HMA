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
        self.budget = 2000
        self.parent = parent

        back = tk.Button(self, text="< back", command=lambda: controller.show_frame(StartPage))
        balance_label = tk.Label(self, text='Current balance: {}'.format(self.budget), font=LARGE_FONT)
        self.exp_tree = ttk.Treeview(self, columns=('id', 'Expense', 'Amount', 'Date'), show='headings',
                                     selectmode='browse')
        self.exp_tree.heading('#1', text='id', anchor=tk.CENTER)
        self.exp_tree.heading('#2', text='Expense', anchor=tk.CENTER)
        self.exp_tree.heading('#3', text='Amount', anchor=tk.CENTER)
        self.exp_tree.heading('#4', text='Date', anchor=tk.CENTER)
        self.exp_tree.column('#1', width=100, stretch=tk.NO)
        self.exp_tree.column('#2', width=200, stretch=tk.NO)
        self.exp_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.exp_tree.column('#4', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.exp_tree["displaycolumns"] = ('Expense', 'Amount', 'Date')
        self.exp_tree.bind('<ButtonRelease-1>', self.activate_exp_button)

        self.inc_tree = ttk.Treeview(self, columns=('id', 'Income', 'Amount', 'Date'), show='headings',
                                     selectmode='browse')
        self.inc_tree.heading('#1', text='id', anchor=tk.CENTER)
        self.inc_tree.heading('#2', text='Income', anchor=tk.CENTER)
        self.inc_tree.heading('#3', text='Amount', anchor=tk.CENTER)
        self.inc_tree.heading('#4', text='Date', anchor=tk.CENTER)
        self.inc_tree.column('#1', width=200, stretch=tk.NO)
        self.inc_tree.column('#2', width=200, stretch=tk.NO)
        self.inc_tree.column('#3', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.inc_tree.column('#4', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.inc_tree["displaycolumns"] = ('Income', 'Amount', 'Date')
        self.inc_tree.bind('<ButtonRelease-1>', self.activate_inc_button)

        self.exp_tree.insert('', 'end', iid=1, values=(1, 'Rent', '1200', '2019-01-01'))
        self.exp_tree.insert('', 'end', text='', values=(1, 'Rent2', '2200', '2019-01-02'))
        self.exp_tree.insert('', 'end', text='', values=(1, 'Rent3', '200', '2019-01-03'))
        self.inc_tree.insert('', 'end', text='', values=(1, 'Salary', '2200', '2019-01-04'))
        self.inc_tree.insert('', 'end', text='', values=(1, 'Salary2', '100', '2019-01-05'))
        self.inc_tree.insert('', 'end', text='', values=(1, 'Salary3', '1500', '2019-01-06'))

        self.exp_add_button = tk.Button(self, text="Add expense", command=self.add_exp_window)
        self.exp_upd_button = tk.Button(self, text="Update expense", state='disabled',
                                        command=lambda: self.update_exp_window(self.exp_tree.focus()))
        self.exp_del_button = tk.Button(self, text="Delete expense", state='disabled',
                                        command=self.delete_exp_window)

        self.inc_add_button = tk.Button(self, text="Add income", command=lambda: self.add_inc_window())
        self.inc_upd_button = tk.Button(self, text="Update income", state='disabled',
                                        command=lambda: self.update_inc_window(self.inc_tree.focus()))
        self.inc_del_button = tk.Button(self, text="Delete income", state='disabled',
                                        command=self.delete_inc_window)

        back.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        balance_label.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        self.exp_tree.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.inc_tree.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.exp_add_button.grid(row=2, column=0, sticky='nsew', padx=5)
        self.exp_upd_button.grid(row=3, column=0, sticky='nsew', padx=5)
        self.exp_del_button.grid(row=4, column=0, sticky='nsew', padx=5)
        self.inc_add_button.grid(row=2, column=1, sticky='nsew', padx=5)
        self.inc_upd_button.grid(row=3, column=1, sticky='nsew', padx=5)
        self.inc_del_button.grid(row=4, column=1, sticky='nsew', padx=5)

    def activate_exp_button(self, event):
        """
        Event handler that enables usage of update and delete buttons only after selecting one of items in expenses list
        :param event:
        :return: None
        """
        if self.exp_tree.focus() == '':
            return
        self.exp_upd_button.configure(state='normal')
        self.exp_del_button.configure(state='normal')

    def activate_inc_button(self, event):
        """
        Event handler that enables usage of update and delete buttons only after selecting one of items in incomes list
        :param event:
        :return: None
        """
        if self.inc_tree.focus() == '':
            return
        self.inc_upd_button.configure(state='normal')
        self.inc_del_button.configure(state='normal')

    def deactivate_exp_button(self):
        """
        Function used to deactivate update and delete buttons after deleting items in expenses list
        :return: None
        """
        self.exp_upd_button.configure(state='disabled')
        self.exp_del_button.configure(state='disabled')

    def deactivate_inc_button(self):
        """
        Function used to deactivate update and delete buttons after deleting items in incomes list
        :return:
        """
        self.inc_upd_button.configure(state='disabled')
        self.inc_del_button.configure(state='disabled')

    def add_exp_window(self):
        """
        Handles configuration of window used to add new item to expenses list
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=10, pady=10)
        window.title('Add expense')
        window.save['command'] = window.add_exp
        window.date_entry.insert(0, str(date.today()))

    def add_inc_window(self):
        """
        Handles configuration of window used to add new item to incomes list
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=10, pady=10)
        window.title('Add income')
        window.save['command'] = window.add_inc
        window.date_entry.insert(0, str(date.today()))

    def update_exp_window(self, iid):
        """
        Handles configuration of window used to update item selected from expenses list
        :param iid: (int) unique number that represents position of item in list
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=20, pady=20)
        window.title('Update expense')
        window.save['command'] = lambda: window.update_exp(iid)

        item = self.exp_tree.item(iid)
        window.name_entry.insert(0, item['values'][1])
        window.amount_entry.insert(0, item['values'][2])
        window.date_entry.insert(0, item['values'][3])

    def update_inc_window(self, iid):
        """
        Handles configuration of window used to update item selected from incomes list
        :param iid: (int) unique number that represents position of item in list
        :return: None
        """
        window = AddUpdateElementWindow(self, padx=20, pady=20)
        window.title('Update income')
        window.save['command'] = lambda: window.update_inc(iid)
        item = self.inc_tree.item(iid)
        window.name_entry.insert(0, item['values'][1])
        window.amount_entry.insert(0, item['values'][2])
        window.date_entry.insert(0, item['values'][3])

    def delete_exp_window(self):
        """
        Handles configuration of window used to delete item from expenses list
        :return: None
        """
        window = DeleteElementWindow(self, padx=10, pady=10)
        window.title('Delete element?')
        window.delete['command'] = lambda: window.delete_exp(self.exp_tree.focus())

    def delete_inc_window(self):
        """
        Handles configuration of window used to delete item from incomes list
        :return: None
        """
        window = DeleteElementWindow(self, padx=10, pady=10)
        window.title('Delete element?')
        window.delete['command'] = lambda: window.delete_inc(self.inc_tree.focus())


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

    def add_exp(self):
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        exp_date = self.date_entry.get()
        self.parent.exp_tree.insert('', 'end', values=(1, name, amount, exp_date))
        self.destroy()

    def update_exp(self, iid):
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        exp_date = self.date_entry.get()
        index = self.parent.exp_tree.index(iid)
        self.parent.exp_tree.delete(iid)
        self.parent.exp_tree.insert('', index, iid=iid, values=(1, name, amount, exp_date))
        self.destroy()

    def add_inc(self):
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        inc_date = self.date_entry.get()
        self.parent.inc_tree.insert('', 'end', values=(1, name, amount, inc_date))
        self.destroy()

    def update_inc(self, iid):
        # todo validation
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        inc_date = self.date_entry.get()
        index = self.parent.inc_tree.index(iid)
        self.parent.inc_tree.delete(iid)
        self.parent.inc_tree.insert('', index, iid=iid, values=(1, name, amount, inc_date))
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

    def delete_exp(self, iid):
        self.parent.exp_tree.delete(iid)
        self.parent.deactivate_exp_button()
        self.destroy()

    def delete_inc(self, iid):
        self.parent.inc_tree.delete(iid)
        self.parent.deactivate_inc_button()
        self.destroy()

        
if __name__ == "__main__":
    app = App()
    app.mainloop()
