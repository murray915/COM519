import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import login_window as lw
import utility_functions as uf
from icecream import ic

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tab Widget")
        self.geometry(uf.get_settings_data()["ktinker_settings"]["app_geometry"])
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")

        ttk.Label(self.tab1, text="This is Tab 1").pack(pady=20)
        ttk.Label(self.tab2, text="This is Tab 2").pack(pady=20)
        ttk.Label(self.tab3, text="This is Tab 3").pack(pady=20)
        
        # Track last selected tab index
        self.last_tab = 0

        # Bind event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def run(self):
        self.mainloop()

    def on_tab_change(self, event):
        new_tab = self.notebook.index("current")

        # Prompt user
        answer = messagebox.askyesno(
            "Switch Tabs?",
            f"Are you sure you want to switch to Tab {new_tab + 1}?"
        )

        if not answer:
            # User cancelled → revert to previous tab
            self.notebook.select(self.last_tab)
            return

        # Accept new tab → update last_tab
        self.last_tab = new_tab