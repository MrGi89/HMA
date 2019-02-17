import tkinter as tk
from frames.landing_frame import LandingFrame
from frames.budget_frame import BudgetFrame
from frames.cook_frame import CookBookFrame


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'HMA - Home Management Application')
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.init_menu(container)

        self.frames = dict()
        for item in (LandingFrame, BudgetFrame, CookBookFrame):
            frame = item(container, self)
            frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            self.frames[item] = frame
        self.show_frame(LandingFrame)

    def init_menu(self, container):
        menu_bar = tk.Menu(container)
        file = tk.Menu(menu_bar, tearoff=0)
        options = tk.Menu(menu_bar, tearoff=0)
        about = tk.Menu(menu_bar, tearoff=0)

        file.add_command(label="Menu", command=lambda: self.show_frame(LandingFrame))
        file.add_separator()
        file.add_command(label="Exit", command=quit)

        menu_bar.add_cascade(label="File", menu=file)
        menu_bar.add_cascade(label="Options", menu=options)
        menu_bar.add_cascade(label="About", menu=about)

        tk.Tk.config(self, menu=menu_bar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont in (BudgetFrame, CookBookFrame):
            frame.refresh_frame()
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
