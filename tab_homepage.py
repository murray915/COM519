import tkinter as tk
import utility_functions as uf
from tkinter import ttk
from tkinter import PhotoImage
from prettytable import PrettyTable


class Tab1(ttk.Frame):    
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.prev_bookings = 0
        self.upcoming_bookings = 0
        self.car_list = 0

        self.curr_user = curr_user
        self.tab_name = "Homepage"
        self.controller = controller
        
        self.table_1 = ""
        self.table_2 = ""
        self.txt_table_1 = None
        self.txt_table_2 = None

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # close app button
        close_app_button = tk.Button(
            self.frame,
            text="Close Application",
            command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)

        # frame 1 - photo
        photo_info_frame = tk.LabelFrame(
            self.frame, text="Welcome to the Garage Booking App"
        )
        photo_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # background image
        self.image = PhotoImage(file=".\images\output-onlinepngtools.png")
        tk.Label(photo_info_frame, image=self.image).grid(
            row=1, column=1, rowspan=3, padx=10, pady=10
        )
        
        ttk.Label(photo_info_frame, text=(
            "This application allows you to book availble services from local garages "
            "\n\n > Please select the Booking Tab to book a service/appointment if you know where & what you want"
            "\n\n > Please select the Account Tab to update any Account Data"
        )).grid(row=1, column=0)
        
        # frame 2 - User Account Info
        user_info_frame = tk.LabelFrame(
            self.frame, 
            text="Notifications    \t\t\t\t\t\tFuture Bookings  \t\t\t\t\t\tCompleted Bookings"
        )
        user_info_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # initial table data
        self.get_table_data()

        # Table 1 
        text_frame_1 = tk.Frame(user_info_frame)
        text_frame_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.txt_table_1 = tk.Text(
            text_frame_1, 
            font=("Courier New", 10), 
            width=80, 
            height=15, 
            wrap="none"
        )

        scroll_y1 = tk.Scrollbar(text_frame_1, orient="vertical", command=self.txt_table_1.yview)
        scroll_x1 = tk.Scrollbar(text_frame_1, orient="horizontal", command=self.txt_table_1.xview)
        self.txt_table_1.configure(yscrollcommand=scroll_y1.set, xscrollcommand=scroll_x1.set)

        self.txt_table_1.grid(row=0, column=0, sticky="nsew")
        scroll_y1.grid(row=0, column=1, sticky="ns")
        scroll_x1.grid(row=1, column=0, sticky="ew")

        self.txt_table_1.insert("1.0", self.table_1)
        self.txt_table_1.config(state="disabled")

        # Table 2
        text_frame_2 = tk.Frame(user_info_frame)
        text_frame_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.txt_table_2 = tk.Text(
            text_frame_2, 
            font=("Courier New", 10), 
            width=80, 
            height=15, 
            wrap="none"
        )

        scroll_y2 = tk.Scrollbar(text_frame_2, orient="vertical", command=self.txt_table_2.yview)
        scroll_x2 = tk.Scrollbar(text_frame_2, orient="horizontal", command=self.txt_table_2.xview)
        self.txt_table_2.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)

        self.txt_table_2.grid(row=0, column=0, sticky="nsew")
        scroll_y2.grid(row=0, column=1, sticky="ns")
        scroll_x2.grid(row=1, column=0, sticky="ew")

        self.txt_table_2.insert("1.0", self.table_2)
        self.txt_table_2.config(state="disabled")


    def on_show(self):
        """Called whenever this tab becomes active"""
        success = self.get_table_data()
        if success:
            # Update Table 1
            self.txt_table_1.config(state="normal")
            self.txt_table_1.delete("1.0", "end")
            self.txt_table_1.insert("1.0", self.table_1)
            self.txt_table_1.config(state="disabled")

            # Update Table 2
            self.txt_table_2.config(state="normal")
            self.txt_table_2.delete("1.0", "end")
            self.txt_table_2.insert("1.0", self.table_2)
            self.txt_table_2.config(state="disabled")

    def get_user_info(self):
        """get booking data (prev/upcoming) and car data"""
        pass

    def get_table_data(self) -> bool:
        """
        update self.table_1 / self.table_2 with data from bookings
        returns True if successful, False otherwise
        """
        conn = None
        try:
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            for i, statement in enumerate(sql_statements):

                # get user_name
                if i == 0:
                    user_name = conn.query(statement, (self.curr_user,))

                # get table 1 data
                elif i == 1:
                    data = conn.query(statement, (user_name[1][0][0],))
                    self.table_1 = PrettyTable()
                    self.table_1.field_names = [
                        "Login Name", "Booking Ref", "Date of Booking", "Garage Name",
                        "Customer Vehicle Reg", "Package", "Payment Method", "Stats", "Total Paid (Inc VAT)"
                    ]
                    for row in data[1]:
                        self.table_1.add_row(row)
                    self.table_1 = self.table_1.get_string()

                # get table 2 data
                elif i == 2:
                    data = conn.query(statement, (user_name[1][0][0],))
                    self.table_2 = PrettyTable()
                    self.table_2.field_names = [
                        "Login Name", "Booking Ref", "Date of Booking", "Garage Name",
                        "Customer Vehicle Reg", "Package", "Payment Method", "Stats", "Total Paid (Inc VAT)"
                    ]
                    for row in data[1]:
                        self.table_2.add_row(row)
                    self.table_2 = self.table_2.get_string()

            if conn:
                conn.close(False)

            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            return False
