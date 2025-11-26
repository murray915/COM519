import tkinter as tk
from tkinter import ttk

class Tab2(ttk.Frame):
    def __init__(self, parent, curr_user):
        super().__init__(parent)

        self.curr_user = curr_user
        self.tab_name = "Book Appointments"

        ttk.Label(self, text="This is Tab 2").pack(pady=20)