import tkinter as tk
import login_window as lw
import utility_functions as uf

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(uf.get_settings_data()["ktinker_settings"]["geometry"])
        self.title('Main Window')

        # place a button on the man window
        tk.Button(self,text='login_window', command=self.open_window).pack(expand=True)

    def open_window(self):
        window = lw.Login_Window(self)
        #for visibility on top level
        window.grab_set()