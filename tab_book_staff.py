import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
from datetime import date 
from datetime import datetime
import utility_functions as uf

class Tab8(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.garage_id = None
        
        self.tab_name = "Complete Bookings"
        self.controller = controller
        
        ttk.Label(self, text="This is the Booking Completion Tab" \
        "\n> This booking table is populated based on the user (staff), primary garage. To change / view other garages, please update user account."
        ).pack(pady=20)


        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Item Info
        # row 0, col 0
        self.booking_data_staff_form = self.frame_1()

        self.load_table_data()

        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=1)


    def frame_1(self):
        """
        constructor for frame 1 : booking_data_staff_form
        """

        booking_data_staff_form = tk.LabelFrame(self.frame, text="Booking Information - For Garage")
        booking_data_staff_form.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # config frame to grid
        booking_data_staff_form.grid_rowconfigure(0, weight=1)
        booking_data_staff_form.grid_columnconfigure(1, weight=1)

        # create subframe for table
        table_frame = tk.Frame(booking_data_staff_form)
        table_frame.grid(row=0, column=0, sticky="nsew")
        
        # create tree
        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "Login Name", "Booking Ref", "Date of Booking", "Garage Name",
                "Customer Vehicle Reg", "Package Name", "Payment Method/Status", "Garage email", "Garage Phone Number",
                "Garage Contact Member of Staff"
            ),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=150)

        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # allow table frame to expand treeview
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # create field frame
        fields_frame = tk.Frame(booking_data_user_form)
        fields_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # config label & entry columns within frame
        fields_frame.grid_columnconfigure(0, weight=0) 
        fields_frame.grid_columnconfigure(1, weight=0) 

        # entrees
        # for edit/cancel 
        self.login_name_var     = tk.StringVar()
        self.booking_ref_var    = tk.StringVar()
        self.date_booking_var   = tk.StringVar()
        self.garage_name_var    = tk.StringVar()
        self.car_reg_var        = tk.StringVar()
        self.package_var        = tk.StringVar()
        self.paymethod_Status   = tk.StringVar()
        self.garage_email       = tk.StringVar()
        self.garage_no          = tk.StringVar()
        self.garage_contact     = tk.StringVar()

        # label params
        # for edit/cancel
        labels = [
            "Login Name :", "Booking Ref :", "Date of Booking :", "Garage Name :",
            "Customer Vehicle Reg :", "Package Name :", "Payment Method/Status :", "Garage email :", "Garage Phone Number :",
            "Garage Contact Member of Staff : "
        ]

        # set fields to be edit/non-edit
        # for edit/cancel
        NO_ENTRY_FIELDS = {0, 1, 3, 5, 6, 7, 8, 9}

        # vars
        # for edit/cancel
        vars = [
            self.login_name_var, self.booking_ref_var, self.date_booking_var,
            self.garage_name_var, self.car_reg_var, self.package_var, self.paymethod_Status,
            self.garage_email, self.garage_no, self.garage_contact
        ]

        start_row = 2
        
        # loop to create label/entry on above params
        # for edit/cancel
        for i, (label, var) in enumerate(zip(labels, vars), start=start_row):
            tk.Label(fields_frame, text=label).grid(row=i, column=0, sticky="e", pady=3)

            # if val in list, label, else entry
            if (i - start_row) in NO_ENTRY_FIELDS:
                tk.Label(fields_frame, textvariable=var).grid(row=i, column=1, sticky="w")
            else:
                tk.Entry(fields_frame, textvariable=var).grid(row=i, column=1, sticky="w")

        # setup vars
        self.vehicle_list           = None
        self.package_list           = None
        self.garage_list            = None
        self.new_referral_txt_var       = tk.StringVar()
        self.new_date_booking_var   = tk.StringVar()

        new_booking_col = 5

        # Create New Booking Date
        tk.Label(fields_frame, text="New Booking Date :").grid(row=start_row, column=new_booking_col, sticky="e", pady=3)
        tk.Entry(fields_frame, textvariable=self.new_date_booking_var).grid(row=start_row, column=new_booking_col + 1, sticky="w")
        
        tk.Label(fields_frame, text="Referral From (online/person...) :").grid(row=start_row + 1, column=new_booking_col, sticky="e", pady=3)
        tk.Entry(fields_frame, textvariable=self.new_referral_txt_var).grid(row=start_row + 1, column=new_booking_col + 1, sticky="w")

        # Dropdown Labels
        tk.Label(fields_frame, text="Dropdown List for Vehicles :").grid(row=start_row + 2, column=new_booking_col, sticky="e")
        tk.Label(fields_frame, text="Dropdown List for Garages :").grid(row=start_row + 3, column=new_booking_col, sticky="e")
        tk.Label(fields_frame, text="Dropdown List for Packages :").grid(row=start_row + 4, column=new_booking_col, sticky="e")

        # Configure expanding columns for new booking inputs
        fields_frame.grid_columnconfigure(new_booking_col + 1, weight=1)
        fields_frame.grid_columnconfigure(new_booking_col + 2, weight=1)

        # Comboboxes
        self.vehicles_combobox = ttk.Combobox(fields_frame, values=self.vehicle_list)
        self.vehicles_combobox.grid(row=start_row + 2, column=new_booking_col + 1, columnspan=2, sticky="ew")

        self.garage_combobox = ttk.Combobox(fields_frame, values=self.garage_list)
        self.garage_combobox.grid(row=start_row + 3, column=new_booking_col + 1, columnspan=2, sticky="ew")

        self.package_combobox = ttk.Combobox(fields_frame, values=self.package_list)
        self.package_combobox.grid(row=start_row + 4, column=new_booking_col + 1, columnspan=2, sticky="ew")

        # buttons
        ttk.Button(fields_frame,text="Save Changes",command=lambda: self.exist_booking_actions("edit")).grid(row=10, column=3, columnspan=2, pady=10)
        ttk.Button(fields_frame,text="Request Cancellation",command=lambda: self.exist_booking_actions("cancel")).grid(row=9, column=3, columnspan=2, pady=10)
        ttk.Button(fields_frame,text="Create Booking",command=self.create_booking).grid(row=9, column=6, columnspan=2, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        return booking_data_user_form
    
    def load_table_data(self) -> tuple[bool, str | None]:
        """
        Docstring for load_table_data. Get all required data
        
        :param self: pull from self params/funcs
        :return: True for succes / False for fail. List of errors (or empty list)
        :rtype: tuple [bool, str | None]
        """
        try:
            conn = None

            # Clear old rows
            for row in self.tree.get_children():
                self.tree.delete(row)

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get user_name
                if i == 0:
                    next_transaction_id = conn.query(sql, ())
                    next_transaction_id = next_transaction_id[1][0][0]

                # get table data
                # future bookings
                if i == 3:
                    rows = conn.query(sql, (user_name[1][0][0],))

            # check for return data
            if rows:
                headers = rows[0]         # headers from sql
                data_rows = rows[1]       # data from sql, list of rows

                for row in data_rows: # get data by row
                    self.tree.insert("", "end", values=row) 

            ########### get all dropdown boxes ##################
            sql = uf.load_sql_file("package_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get package info for dropdown
                if i == 1:
                    all_package_data = conn.query(sql, ())

                    if all_package_data:
                        output_list = []

                        # clean data into list
                        for i in all_package_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.package_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.package_combobox['values'] = self.package_list
                    self.package_combobox.set('')

            sql = uf.load_sql_file("vehicle_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get vehicle info for dropdown
                if i == 1:
                    cus_acc = uf.validate_customer_account(self.curr_user, False)
                    all_veh_data = conn.query(sql, (cus_acc,))

                    if all_veh_data:
                        output_list = []

                        # clean data intp list
                        for i in all_veh_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.vehicle_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.vehicles_combobox['values'] = self.vehicle_list
                    self.vehicles_combobox.set('')

            sql = uf.load_sql_file("garage_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get all garage_id data for dropdown
                if i == 1:
                    all_garage_data = conn.query(sql, ())

                    if all_garage_data:
                        output_list = []

                        # clean data intp list
                        for i in all_garage_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.garage_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.garage_combobox['values'] = self.garage_list
                    self.garage_combobox.set('')

            # commit & close
            conn.close(True)            
        
            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

    def on_row_selected(self, event):
        """
        Docstring for on_row_selected
        
        :param self: pull from self params/funcs. On event is selection from user
        """
        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected, "values")

        self.login_name_var.set(values[0])
        self.booking_ref_var.set(values[1])
        self.date_booking_var.set(values[2])
        self.garage_name_var.set(values[3])
        self.car_reg_var.set(values[4])
        self.package_var.set(values[5])
        self.paymethod_Status.set(values[6])
        self.garage_email.set(values[7])
        self.garage_no.set(values[8])
        self.garage_contact.set(values[9])

        self.selected_booking_ref = values[1]
