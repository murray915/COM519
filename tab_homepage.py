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
        
        self.table_1 = None
        self.table_2 = None


        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)

        # frame 1 - photo
        photo_info_frame = tk.LabelFrame(self.frame, text="Welcome to the Garage Booking App")
        photo_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # background image
        self.image = PhotoImage(file=".\images\output-onlinepngtools.png")
        tk.Label(photo_info_frame, image=self.image).grid(row=1, column=1, rowspan=3, padx=10, pady=10)
        
        ttk.Label(photo_info_frame, text=
                  "This application allows you to book availble services from local garages " \
                  "\n\n > Please select the Booking Tab to book a service/appointment if you know where & what you want" \
                  "\n\n > Please select the Stock Tab to see/add items, check stock levels, or deactivate items" \
                  "\n\n > Please select the Garages Tab to see which Garages & services are availble for them" \
                  "\n\n > Please select the Settings Tab to update any Account Data"
                  ).grid(row=1, column=0)
        
        # frame 2 - User Account Info
        user_info_frame = tk.LabelFrame(self.frame, text="Notifications    \t\t\t\t\t\tFuture Bookings  \t\t\t\t\t\tCompleted Bookings")
        user_info_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.get_table_data()

        # Convert table → string
        table_text = self.table_1

        # Frame for scrollbars + text
        text_frame = tk.Frame(user_info_frame)
        text_frame.grid(row=0, column=0, padx=10, pady=10)

        txt = tk.Text(text_frame, 
                    font=("Courier New", 10), 
                    width=80, 
                    height=15, 
                    wrap="none")

        # Scrollbars
        scroll_y = tk.Scrollbar(text_frame, orient="vertical", command=txt.yview)
        scroll_x = tk.Scrollbar(text_frame, orient="horizontal", command=txt.xview)

        txt.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        txt.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        txt.insert("1.0", table_text)
        txt.config(state="disabled")

        # Convert table → string
        table_text = self.table_2

        # Frame for scrollbars + text
        text_frame = tk.Frame(user_info_frame)
        text_frame.grid(row=0, column=1, padx=10, pady=10)

        txt = tk.Text(text_frame, 
                    font=("Courier New", 10), 
                    width=80, 
                    height=15, 
                    wrap="none")

        # Scrollbars
        scroll_y = tk.Scrollbar(text_frame, orient="vertical", command=txt.yview)
        scroll_x = tk.Scrollbar(text_frame, orient="horizontal", command=txt.xview)

        txt.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        txt.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        txt.insert("1.0", table_text)
        txt.config(state="disabled")


    def get_user_info(self):
        """
        get booking data (prev/upcoming) and cardata
        update respective self. per
        """
        pass


    def get_table_data(self) -> tuple[bool, str | None]:
        """
        update self.table 1/2 with data from bookings

        """
        
        try:
            
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get user_name
                if i == 0:
                    user_name = conn.query(sql, (self.curr_user,))

                # get table 1 data
                if i == 1:
                    data = conn.query(sql, (user_name[1][0][0],))

                    # setup table
                    self.table_1=PrettyTable()
                    self.table_1.field_names = ["Login Name", "Booking Ref", "Date of Booking", "Garage Name", "Customer Vechicle Reg","Package","Parts Quoted/Recieved","QTY of Parts"]

                    # add data to self.table
                    for i in data[1]:
                        self.table_1.add_row(i)

                    self.table_1 = self.table_1.get_string()
            
                # get table 2 data
                if i == 2:
                    data = conn.query(sql, (user_name[1][0][0],))

                    # setup table
                    self.table_2=PrettyTable()
                    self.table_2.field_names = ["Login Name", "Booking Ref", "Date of Booking", "Garage Name", "Customer Vechicle Reg","Package","Parts Quoted/Recieved","QTY of Parts"]

                    # add data to self.table
                    for i in data[1]:
                        self.table_2.add_row(i)

                    self.table_2 = self.table_2.get_string()


            conn.close(False)                        
            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)