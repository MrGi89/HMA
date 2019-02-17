import tkinter as tk
from PIL import Image, ImageTk
import cfg
from frames.budget_frame import BudgetFrame
from frames.cook_frame import CookBookFrame


class LandingFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # FRAME ROWS CONFIGURATION
        for row in range(8):
            self.grid_rowconfigure(row, weight=1)
        self.grid_rowconfigure(1, weight=20)

        # SETTING ELEMENTS
        self.parent = parent
        self.user_label = tk.Label(self, text='Welcome Anonymous')
        self.welcome_label = tk.Label(self,
                                      text='Welcome to HMA - your Home Management Application',
                                      font=('verdana', 12),
                                      wraplength=500)
        self.images = dict()
        self.set_images()
        self.displayed_img = tk.Label(self, image=self.images['home'], height=150, width=200)

        # SETTING BUTTONS
        self.login_btn = tk.Button(self,
                                   text='Sign in',
                                   command=lambda: LoginWindow(self, padx=20, pady=20))
        self.register_btn = tk.Button(self,
                                      text='Create new account',
                                      command=lambda: RegisterWindow(self, padx=20, pady=20))
        self.budget_btn = tk.Button(self,
                                    text='Manage your budget',
                                    state='disabled',
                                    command=lambda: self.parent.master.show_frame(BudgetFrame))
        self.cook_book_btn = tk.Button(self,
                                       text='Show your recipes',
                                       state='disabled',
                                       command=lambda: self.parent.master.show_frame(CookBookFrame))
        self.task_btn = tk.Button(self,
                                  text='Check your tasks',
                                  state='disabled')
        self.exit_btn = tk.Button(self,
                                  text='Exit',
                                  command=quit)

        # ADDS EVENT LISTENERS
        self.login_btn.bind('<Enter>', self.show_login_img)
        self.login_btn.bind('<Leave>', self.show_home_img)
        self.register_btn.bind('<Enter>', self.show_register_img)
        self.register_btn.bind('<Leave>', self.show_home_img)
        self.budget_btn.bind('<Enter>', self.show_budget_img)
        self.budget_btn.bind('<Leave>', self.show_home_img)
        self.cook_book_btn.bind('<Enter>', self.show_cook_book_img)
        self.cook_book_btn.bind('<Leave>', self.show_home_img)
        self.task_btn.bind('<Enter>', self.show_task_img)
        self.task_btn.bind('<Leave>', self.show_home_img)
        self.exit_btn.bind('<Enter>', self.show_exit_img)
        self.exit_btn.bind('<Leave>', self.show_home_img)

        # STYLING
        self.user_label.grid(column=1, row=0, padx=1, pady=0, sticky='e')
        self.welcome_label.grid(column=0, row=1, columnspan=2, padx=1, pady=0, sticky='nsew')
        self.displayed_img.grid(column=1, row=2, rowspan=6, padx=1, pady=0, sticky='nsew')
        self.login_btn.grid(column=0, row=2, padx=1, pady=0, sticky='nsew')
        self.register_btn.grid(column=0, row=3, padx=1, pady=0, sticky='nsew')
        self.budget_btn.grid(column=0, row=4, padx=1, pady=0, sticky='nsew')
        self.cook_book_btn.grid(column=0, row=5, padx=1, pady=0, sticky='nsew')
        self.task_btn.grid(column=0, row=6, padx=1, pady=0, sticky='nsew')
        self.exit_btn.grid(column=0, row=7, padx=1, pady=0, sticky='nsew')

    def show_login_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['login'])
        self.displayed_img.image = self.images['login']

    def show_register_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['register'])
        self.displayed_img.image = self.images['register']

    def show_home_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['home'])
        self.displayed_img.image = self.images['home']

    def show_budget_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['budget'])
        self.displayed_img.image = self.images['budget']

    def show_cook_book_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['cook'])
        self.displayed_img.image = self.images['cook']

    def show_task_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['task'])
        self.displayed_img.image = self.images['task']

    def show_exit_img(self, event):
        """
        Event handler responsible for changing image
        :param event: not used
        :return: None
        """
        self.displayed_img.configure(image=self.images['exit'])
        self.displayed_img.image = self.images['exit']

    def set_images(self):
        """
        Loads and configures images, saves them to self.images class attribute
        :return: None
        """
        for file in ('home', 'login', 'register', 'budget', 'cook', 'task', 'exit'):
            img = Image.open('static/{}.jpg'.format(file))
            img = img.resize((180, 180), Image.ANTIALIAS)
            self.images[file] = ImageTk.PhotoImage(img)

    def login(self, user):

        cfg.CURRENT_USER = user
        self.user_label.configure(text='Welcome {}'.format(user['username'].capitalize()))
        self.login_btn.configure(text='Logout', command=self.logout)
        self.register_btn.configure(state='disabled')
        self.cook_book_btn.configure(state='normal')
        self.budget_btn.configure(state='normal')

    def logout(self):

        cfg.CURRENT_USER['id'] = None
        cfg.CURRENT_USER['username'] = None
        self.user_label.configure(text='Welcome Anonymous')
        self.login_btn.configure(text='Sign in',
                                 command=lambda: LoginWindow(self, padx=10, pady=10))
        self.register_btn.configure(state='normal')
        self.cook_book_btn.configure(state='disabled')
        self.budget_btn.configure(state='disabled')


class LoginWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)
        self.title('Sign in')
        self.parent = parent

        # SETTING ELEMENTS
        self.username_lbl = tk.Label(self, text='Username')
        self.username_val = tk.Entry(self)
        self.password_lbl = tk.Label(self, text='Password')
        self.password_val = tk.Entry(self, show='*')
        self.login_btn = tk.Button(self, text='Sign in', command=self.authenticate)

        # STYLING
        self.username_lbl.grid(column=0, row=0, padx=2, pady=2, sticky='nsew')
        self.username_val.grid(column=1, row=0, padx=2, pady=2, sticky='nsew')
        self.password_lbl.grid(column=0, row=1, padx=2, pady=2, sticky='nsew')
        self.password_val.grid(column=1, row=1, padx=2, pady=2, sticky='nsew')
        self.login_btn.grid(column=0, row=2, columnspan=2, padx=2, pady=2, sticky='nsew')

    def authenticate(self):
        """
        Validate user input, authenticate user and saves his details to CURRENT_USER global variable
        :return: None
        """
        # VALIDATES USERNAME
        username = self.username_val.get()
        if not username:
            cfg.ValidationError(self, text='Username can\'t be empty!', padx=10, pady=10)
            return
        user = cfg.db_execute(
            sql='''SELECT * FROM users WHERE username=?;''',
            variables=(username,),
            cursor_type='fetchone')
        if user is None:
            cfg.ValidationError(self, text='Incorrect username or password!', padx=10, pady=10)
            return
        # todo hash password
        # VALIDATES PASSWORD
        password = self.password_val.get()
        if not password or password != user['password']:
            cfg.ValidationError(self, text='Incorrect username or password!', padx=10, pady=10)
            return
        # LOGS USER
        self.parent.login({'id': user['id'], 'username': user['username']})
        self.destroy()


class RegisterWindow(tk.Toplevel):

    def __init__(self, parent, **kwargs):
        tk.Toplevel.__init__(self, parent, **kwargs)
        self.title('New account')
        self.parent = parent

        # SETTING ELEMENTS
        self.username_lbl = tk.Label(self, text='Username')
        self.username_val = tk.Entry(self)
        self.password_lbl = tk.Label(self, text='Password')
        self.password_val = tk.Entry(self)
        self.password_conf_lbl = tk.Label(self, text='Password')
        self.password_conf_val = tk.Entry(self)
        self.register_btn = tk.Button(self, text='Sign on', command=self.create_user)

        # STYLING
        self.username_lbl.grid(column=0, row=0, padx=2, pady=2, sticky='nsew')
        self.username_val.grid(column=1, row=0, padx=2, pady=2, sticky='nsew')
        self.password_lbl.grid(column=0, row=1, padx=2, pady=2, sticky='nsew')
        self.password_val.grid(column=1, row=1, padx=2, pady=2, sticky='nsew')
        self.password_conf_lbl.grid(column=0, row=2, padx=2, pady=2, sticky='nsew')
        self.password_conf_val.grid(column=1, row=2, padx=2, pady=2, sticky='nsew')
        self.register_btn.grid(column=0, row=3, columnspan=2, padx=2, pady=2, sticky='nsew')

    def validate_input(self):
        """
        Validate user input
        :return: tuple containing validated data, None if data was incorrect
        """
        # VALIDATES USERNAME
        username = self.username_val.get()
        if not username:
            cfg.ValidationError(self, text='Username can\'t be empty!', padx=10, pady=10)
            return
        users = cfg.db_execute(
            sql='''SELECT username FROM users WHERE username=?;''',
            variables=(username,))
        if users:
            cfg.ValidationError(self, text='Username is occupied by another user', padx=10, pady=10)
            return
        # VALIDATES PASSWORDS
        password = self.password_val.get()
        password_conf = self.password_conf_val.get()
        if not password:
            cfg.ValidationError(self, text='Password can\'t be empty!', padx=10, pady=10)
            return
        if password != password_conf:
            cfg.ValidationError(self, text='Passwords do not match!', padx=10, pady=10)
            return
        return username, password

    def create_user(self):
        """
        Saves user to DB and logs by saving user details to CURRENT_USER global variable
        :return: None
        """
        user = self.validate_input()
        # todo hash password
        if user:
            user_id = cfg.db_execute(
                sql='''INSERT INTO users VALUES (NULL, ?, ?);''',
                variables=(user[0], user[1]),
                cursor_type='lastrowid')
            # LOGS USER
            self.parent.login({'id': user_id, 'username': user[0]})
            self.destroy()
