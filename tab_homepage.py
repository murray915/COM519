import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from prettytable import PrettyTable

class Tab1(ttk.Frame):    
    def __init__(self, parent, curr_user):
        super().__init__(parent)

        self.prev_bookings = 0
        self.upcoming_bookings = 0
        self.car_list = 0

        self.curr_user = curr_user
        self.tab_name = "Homepage"

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - photo
        photo_info_frame = tk.LabelFrame(self.frame, text="Welcome to the Garage Booking App")
        photo_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # background image
        self.image = PhotoImage(file=".\images\output-onlinepngtools.png")
        tk.Label(photo_info_frame, image=self.image).grid(row=1, column=1, rowspan=3, padx=10, pady=10)
        
        ttk.Label(photo_info_frame, text=
                  "This application allows you to book availble services from local garages " \
                  "\n\n > Please select the Booking Tab to book a service/appointment if you know where & what you want" \
                  "\n\n > Please select the Garages Tab to see which Garages & services are availble for them" \
                  "\n\n > Please select the Settings Tab to update any Account Data"
                  ).grid(row=1, column=0)
        
        # frame 2 - User Account Info
        user_info_frame = tk.LabelFrame(self.frame, text="Notifications")
        user_info_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        x=PrettyTable()
        x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]

        x.add_row(["Adelaide", 1295, 1158259, 600.5])
        x.add_row(["Brisbane", 5905, 1857594, 1146.4])
        x.add_row(["Darwin", 112, 120900, 1714.7])
        x.add_row(["Hobart", 1357, 205556, 619.5])
        x.add_row(["Sydney", 2058, 4336374, 1214.8])
        x.add_row(["Melbourne", 1566, 3806092, 646.9])
        x.add_row(["Perth", 5386, 1554769, 869.4])

        # Convert table → string
        table_text = x.get_string()

        # Use Text widget instead of Label
        txt = tk.Text(user_info_frame, font=("Courier New", 10), width=60, height=12)
        txt.insert("1.0", table_text)
        txt.config(state="disabled")
        txt.grid(row=0, column=0, padx=10, pady=10)

        y=PrettyTable()
        y.field_names = ["City name", "Area", "Population", "Annual Rainfall"]

        y.add_row(["Adelaide", 1295, 1158259, 600.5])
        y.add_row(["Brisbane", 5905, 1857594, 1146.4])
        y.add_row(["Darwin", 112, 120900, 1714.7])
        y.add_row(["Hobart", 1357, 205556, 619.5])
        y.add_row(["Sydney", 2058, 4336374, 1214.8])
        y.add_row(["Melbourne", 1566, 3806092, 646.9])
        y.add_row(["Perth", 5386, 1554769, 869.4])

        # Convert table → string
        table_text_2 = y.get_string()

        # Use Text widget instead of Label
        txt = tk.Text(user_info_frame, font=("Courier New", 10), width=60, height=12)
        txt.insert("1.0", table_text_2)
        txt.config(state="disabled")
        txt.grid(row=0, column=1, padx=10, pady=10)


    def get_user_info(self):
        """
        get booking data (prev/upcoming) and cardata
        update respective self. per
        """
        pass