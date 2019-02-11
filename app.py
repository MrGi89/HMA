import tkinter as tk
from budget_page import BudgetPage
from cook_page import CookPage

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
        for item in (StartPage, BudgetPage, CookPage):
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
        tk.Button(self,
                  text="Budget",
                  height=1,
                  font=MEDIUM_FONT,
                  command=lambda: controller.show_frame(BudgetPage)).pack(fill='both', pady=5)
        tk.Button(self, text="Shopping list", height=1, font=MEDIUM_FONT, state='disabled').pack(fill='both', pady=5)
        tk.Button(self,
                  text="Cook book",
                  height=1,
                  font=MEDIUM_FONT,
                  command=lambda: controller.show_frame(CookPage)).pack(fill='both', pady=5)
        tk.Button(self, text="Exit", height=1, font=MEDIUM_FONT, command=quit).pack(fill='both', pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
