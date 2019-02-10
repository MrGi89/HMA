import tkinter as tk
from tkinter import ttk
from tools import db_execute

MEDIUM_FONT = ("verdana", 12)
LARGE_FONT = ("verdana", 16)


class CookPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # SETTING ELEMENTS
        self.parent = parent
        self.search = tk.Entry(self)
        self.search.insert(0, 'search...')
        self.list = ttk.Treeview(self, columns=('id', 'title', 'desc'), show='headings', selectmode='browse')
        self.list.heading('#2', text='Recipes', anchor=tk.CENTER)
        self.list.column('#2', stretch=tk.NO, anchor=tk.W)
        self.list['displaycolumns'] = ('title', )
        self.add = tk.Button(self, text='Add recipe', command=self.add_window)
        self.update = tk.Button(self, text='Update recipe', command=lambda: self.update_window(self.list.focus()))
        self.delete = tk.Button(self, text='Delete recipe')
        self.recipe = tk.Frame(self)

        # RECIPE FRAME CONFIGURATION
        welcome_recipe = Recipe(self.recipe,
                                self,
                                title='Choose recipe',
                                desc='To see details choose one of available recipes from list on the left')
        welcome_recipe.grid(row=0, column=0, sticky='nsew')
        self.recipes = {0: welcome_recipe}
        for item in CookPage.get_recipes():
            frame = Recipe(self.recipe,
                           self,
                           title=item['title'],
                           desc=item['desc'])
            frame.grid(row=0, column=0, sticky='nsew')
            self.recipes[item['id']] = frame
            # ADDS ELEMENTS TO RECIPES TREE
            self.list.insert('', 'end', values=(item['id'], item['title'], item['desc']))
        # ADDS EVENT LISTENER TO RECIPES TREE
        self.list.bind('<ButtonRelease-1>', self.change_frame)
        self.show_frame(0)

        # STYLING
        self.add.grid(row=0, column=0, padx=5, pady=1, sticky='nsew')
        self.update.grid(row=1, column=0, padx=5, pady=1, sticky='nsew')
        self.delete.grid(row=2, column=0, padx=5, pady=1, sticky='nsew')
        self.search.grid(row=3, column=0, padx=5, pady=1, sticky='nsew')
        self.list.grid(row=4, column=0, padx=5, pady=1, sticky='nsew')
        self.recipe.grid(row=0, column=1, rowspan=5, padx=5, sticky='nsew')

    def change_frame(self, event):
        """
        Event listener that cathes request for recipe change
        :param event: not used
        :return: None
        """
        iid = self.list.focus()
        if iid == '':
            return
        item = self.list.item(iid)
        self.show_frame(item['values'][0])

    def show_frame(self, recipe_id):
        """
        Handles changing of frame
        :param recipe_id: (int) ID of selected recipe in DB
        :return: None
        """
        frame = self.recipes[recipe_id]
        frame.tkraise()

    @staticmethod
    def get_recipes(query=None):
        if query:
            recipes = db_execute(
                sql='''SELECT * FROM recipes WHERE title LIKE ?;''',
                variables=(query, ))
        else:
            recipes = db_execute(sql='''SELECT * FROM recipes;''')
        return recipes if recipes else list()

    def add_window(self):
        window = AddUpdateWindow(self, padx=10, pady=10)
        window.title('Add recipe')
        window.save['command'] = window.add_recipe

    def update_window(self, iid):
        if iid == '':
            return

        window = AddUpdateWindow(self, padx=10, pady=10)
        window.title('Update recipe')
        item = self.list.item(iid)
        window.title_value.insert(0, item['values'][1])
        window.desc_value.insert(0, item['values'][2])
        window.save['command'] = lambda: window.update_recipe(item['values'][0])

    def delete_window(self):

        pass


class AddUpdateWindow(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.title_label = tk.Label(self, text='Title')
        self.title_value = tk.Entry(self)
        self.desc_label = tk.Label(self, text='Description')
        self.desc_value = tk.Entry(self)
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.save = tk.Button(self, text='Save')

        self.title_label.grid(row=0, column=0, sticky='w', pady=5)
        self.title_value.grid(row=0, column=1, columnspan=2, sticky='e', padx=2)
        self.desc_label.grid(row=1, column=0, sticky='w', pady=5)
        self.desc_value.grid(row=1, column=1, columnspan=2, sticky='e', padx=2)
        self.cancel.grid(row=2, column=1, pady=5, sticky='e')
        self.save.grid(row=2, column=2, pady=5, sticky='e')

    def add_recipe(self):
        """"""
        title = self.title_value.get()
        desc = self.desc_value.get()
        db_execute(sql='''INSERT INTO recipes VALUES (NULL, ?, ?);''',
                   variables=(title, desc))
        self.destroy()

    def update_recipe(self, recipe_id):
        """"""
        title = self.title_value.get()
        desc = self.desc_value.get()
        db_execute(sql='''UPDATE recipes SET title=?, desc=? WHERE id=?;''',
                   variables=(title, desc, recipe_id))
        self.destroy()


class Recipe(tk.Frame):
    def __init__(self, parent, controller, title, desc, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.parent = parent
        self.title = tk.Label(self, text=title, font=LARGE_FONT, wraplength=480)
        self.desc = tk.Label(self, text=desc, wraplength=480, justify='left')

        self.title.grid(row=0, column=0, padx=5, pady=1, sticky='w')
        self.desc.grid(row=1, column=0, padx=5, pady=15, sticky='nsew')
