import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utility_functions as uf
from icecream import ic

from tab_homepage import Tab1
from tab_book_appointments import Tab2
from tab_stock import Tab3
from tab_packages import Tab4


class Main(tk.Tk):
    def __init__(self, curr_user, access_code):
        super().__init__()

        # general params
        self.curr_user = curr_user
        self.access_code = access_code

        # ktinker params
        self.configure(bg="lightgray")
        self.title("Garage Appointment & Service Application")
        self.geometry(uf.get_settings_data()["ktinker_settings"]["app_geometry"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.TNotebook",
            background="lightgray",
            borderwidth=0
        )

        # Tabs background
        style.configure(
            "Custom.TNotebook.Tab",
            background="lightgray",
            padding=[10, 5]
        )

        # Selected tab background
        style.map(
            "Custom.TNotebook.Tab",
            background=[("selected", "white")],
            foreground=[("selected", "black")]
        )

        # For tab content frames
        style.configure("TabFrame.TFrame", background="white")
    

        self.notebook = ttk.Notebook(self, style="Custom.TNotebook")
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.tab1 = Tab1(self.notebook, self.curr_user, "TabFrame.TFrame")
        self.tab2 = Tab2(self.notebook, self.curr_user, "TabFrame.TFrame")
        self.tab3 = Tab3(self.notebook, self.curr_user, "TabFrame.TFrame")
        self.tab4 = Tab4(self.notebook, self.curr_user, "TabFrame.TFrame")

        # Add to Notebook
        self.notebook.add(self.tab1, text=self.tab1.tab_name)
        self.notebook.add(self.tab2, text=self.tab2.tab_name)
        self.notebook.add(self.tab3, text=self.tab3.tab_name)
        self.notebook.add(self.tab4, text=self.tab4.tab_name)

        # Track last selected tab index
        self.last_tab = 0
        self.first_event = True

        # Bind event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # access logic
        if self.access_code == 'CUS_USR':
            #self.notebook.forget(self.tab3)
            pass

        if self.access_code == 'admin':
            pass


    def run(self):
        """
        function to trigger ktinker & loop
        no return values
        """
        self.mainloop()


    def on_tab_change(self, event):
        """
        Func to monitor the change in tabs and prompt users to check
        incase data is not saved
        
        :param event: 
        """
        # Ignore the first automatic event on program start
        if self.first_event:
            self.first_event = False
            return

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