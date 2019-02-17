import tkinter as tk
from tkinter import ttk
import cfg


class CookBookFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # SETTING ELEMENTS
        self.parent = parent
        self.search = tk.Entry(self)
        self.search.insert(0, 'search...')
        self.list = ttk.Treeview(self, columns=('title', 'desc'), show='headings', selectmode='browse')
        self.list.heading('#1', text='Recipes', anchor=tk.CENTER)
        self.list.column('#1', width=210, stretch=tk.NO, anchor=tk.W)
        self.list['displaycolumns'] = ('title',)
        self.add = tk.Button(self,
                             text='Add recipe',
                             command=self.add_window)
        self.update = tk.Button(self,
                                text='Update recipe',
                                state='disabled',
                                command=lambda: self.update_window(self.list.focus()))
        self.delete = tk.Button(self,
                                text='Delete recipe',
                                state='disabled',
                                command=lambda: self.delete_window(self.list.focus()))
        self.recipe = tk.Frame(self)
        self.frames = dict()

        # ADDS EVENT LISTENERS
        self.list.bind('<ButtonRelease-1>', self.change_frame)
        self.search.bind('<FocusIn>', self.clear_search_button_placeholder)
        self.search.bind('<FocusOut>', self.add_search_button_placeholder)
        self.search.bind('<KeyRelease>', self.filter_recipes)

        # STYLING
        self.add.grid(row=0, column=0, padx=5, pady=1, sticky='nsew')
        self.update.grid(row=1, column=0, padx=5, pady=1, sticky='nsew')
        self.delete.grid(row=2, column=0, padx=5, pady=1, sticky='nsew')
        self.search.grid(row=3, column=0, padx=5, pady=1, sticky='nsew')
        self.list.grid(row=4, column=0, padx=5, pady=1, sticky='nsew')
        self.recipe.grid(row=0, column=1, rowspan=5, padx=5, sticky='nsew')

    def refresh_frame(self, query=None):
        """
        Refreshes cook book page data, inserts correct values to list tree
        :param query: (str) data passed by user to filter list tree
        :return: None
        """
        # CLEARS FRAMES DICT AND LIST ELEMENTS
        self.frames.clear()
        self.list.delete(*self.list.get_children())
        if query:
            recipes = cfg.db_execute(
                sql='''SELECT * FROM recipes 
                       WHERE title LIKE ? AND user_id=?
                       ORDER BY title COLLATE NOCASE ASC;''',
                variables=('%' + query + '%', cfg.CURRENT_USER['id']))
        else:
            recipes = cfg.db_execute(
                sql='''SELECT * FROM recipes 
                       WHERE user_id=?
                       ORDER BY title COLLATE NOCASE ASC;''',
                variables=(cfg.CURRENT_USER['id'],))
        # CREATES WELCOME FRAME
        recipes.append({'id': 0,
                        'title': 'Choose recipe',
                        'desc': 'To see details choose one of available recipes from list on the left'})
        # CREATES FRAMES FROM DATA FOUNDED IN DB
        for recipe in recipes:
            frame = Recipe(self.recipe,
                           self,
                           title=recipe['title'],
                           desc=recipe['desc'])
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[recipe['id']] = frame
        # ADDS ELEMENT TO LIST
        for recipe in recipes:
            if recipe['id'] == 0:
                continue
            self.list.insert('', 'end', iid=recipe['id'], values=(recipe['title'].capitalize(), recipe['desc']))

    def clear_search_button_placeholder(self, event):
        """
        Event handler responsible for clearing search bar placeholder
        :param event: not used
        :return: None
        """
        if self.search.get() == 'search...':
            self.search.delete(0, tk.END)

    def add_search_button_placeholder(self, event):
        """
        Event handler responsible for adding placeholder to search bar if it's empty
        :param event: not used
        :return: None
        """
        if self.search.get() == '':
            self.search.insert(0, 'search...')

    def filter_recipes(self, event):
        """
        Event handler responsible for enabling filtering tree list
        :param event: not used
        :return: None
        """
        self.refresh_frame(query=self.search.get())
        self.deactivate_buttons()

    def change_frame(self, event):
        """
        Event listener that catches recipe change request and passes it to frame changer function
        :param event: not used
        :return: None
        """
        iid = self.list.focus()
        if iid == '':
            return
        self.show_frame(int(iid))
        self.activate_buttons()

    def activate_buttons(self):
        """
        Function used to activate update and delete buttons
        :return: None
        """
        self.update.configure(state='normal')
        self.delete.configure(state='normal')

    def deactivate_buttons(self):
        """
        Function used to deactivate update and delete buttons
        :return: None
        """
        self.update.configure(state='disabled')
        self.delete.configure(state='disabled')

    def show_frame(self, recipe_id):
        """
        Handles frame changing
        :param recipe_id: (int) ID of selected recipe in DB
        :return: None
        """
        try:
            frame = self.frames[recipe_id]
        except KeyError:
            frame = self.frames[0]
        frame.tkraise()

    def add_window(self):
        """
        Handles configuration of window used to add element to list tree
        :return: None
        """
        window = AddUpdateWindow(self, padx=10, pady=10)
        window.title('Add recipe')
        window.save['command'] = window.add_recipe

    def update_window(self, recipe_id):
        """
        Handles configuration of window used to update element in list tree
        :param recipe_id: (int) ID of recipe stored in DB
        :return: None
        """
        window = AddUpdateWindow(self, padx=10, pady=10)
        window.title('Update recipe')
        item = self.list.item(recipe_id)
        window.title_value.insert(0, item['values'][0])
        window.desc_value.insert(tk.INSERT, item['values'][1])
        window.save['command'] = lambda: window.update_recipe(recipe_id)

    def delete_window(self, recipe_id):
        """
        Handles configuration of window used to delete list tree element
        :param recipe_id: (int) ID of recipe stored in DB
        :return: None
        """
        window = DeleteWindow(self, padx=10, pady=10)
        window.title('Delete element?')
        window.delete['command'] = lambda: window.delete_recipe(recipe_id=recipe_id)


class AddUpdateWindow(tk.Toplevel):
    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.title_label = tk.Label(self, text='Title')
        self.title_value = tk.Entry(self, width=30)
        self.desc_label = tk.Label(self, text='Description')
        self.desc_value = tk.Text(self, height=10, width=30)
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.save = tk.Button(self, text='Save')

        self.title_label.grid(row=0, column=0, sticky='w', pady=5)
        self.title_value.grid(row=0, column=1, columnspan=2, sticky='e', padx=2)
        self.desc_label.grid(row=1, column=0, sticky='w', pady=5)
        self.desc_value.grid(row=1, column=1, columnspan=2, sticky='e', padx=2)
        self.cancel.grid(row=2, column=1, pady=5, sticky='e')
        self.save.grid(row=2, column=2, pady=5, sticky='e')

    def add_recipe(self):
        """
        Adds new recipe to DB and refreshes page
        :return: None
        """
        validated_data = self.validate_input()
        if validated_data:
            recipe_id = cfg.db_execute(sql='''INSERT INTO recipes VALUES (NULL, ?, ?, ?);''',
                                       variables=(validated_data[0], validated_data[1], cfg.CURRENT_USER['id']),
                                       cursor_type='last_id')
            query = self.parent.search.get()
            if query == 'search...':
                self.parent.refresh_frame()
            else:
                self.parent.refresh_frame(query)

            if self.parent.list.exists(str(recipe_id)):
                self.parent.list.selection_set(str(recipe_id))
                self.parent.list.focus_set()
                self.parent.list.focus(str(recipe_id))
                self.parent.activate_buttons()
            else:
                self.parent.deactivate_buttons()

            self.parent.show_frame(recipe_id)
            self.destroy()

    def update_recipe(self, recipe_id):
        """
        Updates recipe in DB and refreshes page
        :param recipe_id: (int) ID of recipe stored in DB
        :return: None
        """
        validated_data = self.validate_input()
        if validated_data:
            cfg.db_execute(sql='''UPDATE recipes SET title=?, `desc`=? WHERE id=?;''',
                           variables=(validated_data[0], validated_data[1], recipe_id))
            query = self.parent.search.get()
            if query == 'search...':
                self.parent.refresh_frame()
            else:
                self.parent.refresh_frame(query)

            if self.parent.list.exists(recipe_id):
                self.parent.list.selection_set(recipe_id)
                self.parent.list.focus_set()
                self.parent.list.focus(recipe_id)
            else:
                self.parent.deactivate_buttons()
            self.parent.show_frame(int(recipe_id))
            self.destroy()

    def validate_input(self):
        """
        Handles user input data validation. Raises tk.TopLevel widget frame as error if incorrect data is entered
        :return: tuple that stores correct data. None if data was incorrect.
        """
        # VALIDATES TITLE ENTRY
        title = self.title_value.get()
        if title == '':
            cfg.ValidationError(self, text='Recipe title can\'t be empty!', padx=10, pady=10)
            return
        # VALIDATES DESCRIPTION ENTRY
        desc = self.desc_value.get(1.0, tk.END)
        if len(desc) == 1:
            cfg.ValidationError(self, text='Recipe description can\'t be empty!', padx=10, pady=10)
            return
        return title, desc


class Recipe(tk.Frame):
    def __init__(self, parent, controller, title, desc, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.parent = parent
        self.title = tk.Label(self, text=title, font=('verdana', 16), wraplength=480)
        self.desc = tk.Label(self, text=desc, wraplength=480, justify='left')

        self.title.grid(row=0, column=0, padx=5, pady=1, sticky='w')
        self.desc.grid(row=1, column=0, padx=5, pady=15, sticky='nsew')


class DeleteWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)

        self.parent = parent
        self.label = tk.Label(self, text='Are you sure you want to delete this element?')
        self.cancel = tk.Button(self, text='Cancel', command=self.destroy)
        self.delete = tk.Button(self, text='Delete')

        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=5)
        self.cancel.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.delete.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    def delete_recipe(self, recipe_id):
        """
        Deletes recipe from DB and refreshes tree elements
        :param recipe_id: (int) ID of recipe stored in DB
        :return: None
        """
        cfg.db_execute(
            sql='''DELETE FROM recipes WHERE id=?;''',
            variables=(recipe_id,))
        query = self.parent.search.get()
        if query == 'search...':
            self.parent.refresh_frame()
        else:
            self.parent.refresh_frame(query)
        self.parent.show_frame(0)
        self.parent.deactivate_buttons()
        self.destroy()
