import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
from datetime import date 
from datetime import datetime
import utility_functions as uf

class Tab2(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Book Appointments"
        self.controller = controller
        
        ttk.Label(self, text="This is the Book Appointment Tab" \
        "\n> The main display is all current (future) bookings, by Booking date. To edit any booking please select the respective row, and change the required details in the bottom selection, then press 'Save Changes'." \
        "\n> To cancel a booking, please press the 'request cancellation' option, and this will alert the garage to the request, and acceptance and full cancelation should follow."\
        "\n\n> To create new bookings, please input the required date (from Today into the future), and select using the dropdown boxes the package/garage and Vehicle registered with the account"
        ).pack(pady=20)


        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Item Info
        # row 0, col 0
        self.booking_data_user_form = self.frame_1()

        self.load_table_data()

        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=1)


    def frame_1(self):
        """
        constructor for frame 1 : booking_data_user_form
        """

        # create main frame label
        booking_data_user_form = tk.LabelFrame(self.frame, text="Booking Information")
        booking_data_user_form.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # config frame to grid
        booking_data_user_form.grid_rowconfigure(0, weight=1)
        booking_data_user_form.grid_columnconfigure(1, weight=1)

        # create subframe for table
        table_frame = tk.Frame(booking_data_user_form)
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

        # set fields to be edit/non-edit i.e. user input
        # for edit/cancel frame
        NO_ENTRY_FIELDS = {0, 1, 3, 5, 6, 7, 8, 9}

        # vars
        # for edit/cancel frame
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
        self.new_referral_txt_var   = tk.StringVar()
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

    def on_show(self):
        """Called whenever this tab becomes active"""
        print("Refreshing Tab data")
        self.load_table_data()

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
                    user_name = conn.query(sql, (self.curr_user,))

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

            # clear user inputs
            self.new_date_booking_var.set('')
            self.new_referral_txt_var.set('')

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

    def create_booking(self)-> tuple[bool, str | None]:
        """
        Docstring for create_booking
        
        :param self: pull from self params/funcs
        :return: True for succes / False for fail. List of errors (or empty list)
        :rtype: tuple [bool, str | None]
        """
        try:

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):
            
                # get next id
                if i == 8:
                    next_booking_id = conn.query(sql, ())
                    next_booking_id = next_booking_id[1][0][0]

            # sort user input date
            user_input = self.new_date_booking_var.get()
            fixed_date = self.normalise_date(user_input)

            # gather user inputs
            params = (     
                fixed_date,
                self.vehicles_combobox.get(),
                self.garage_combobox.get(),
                self.package_combobox.get()
            )

            # get the inputs
            result = self.check_user_inputs_create(params)
            if result:
                raise ValueError(result)
            
            create_params = ()

            # check if inputs are correct
            if not result:

                # update param with veh_id & reformat date
                booking_date = datetime.strptime(fixed_date, "%d/%m/%Y")
                booking_date_str = booking_date.strftime("%Y-%m-%d")
                
                # get ids from input dropdowns
                # get params for sql
                vehicle_id = params[1].split(" : ")[0]
                garage_id = params[2].split(" : ")[0]
                package_id = params[3].split(" : ")[0]

                # get customer account, if not one. Create and return
                cus_acc = uf.validate_customer_account(self.curr_user, True)

                # check for referral input (not required.)
                if self.new_referral_txt_var.get() is None or self.new_referral_txt_var.get() == '':
                    referral = 0
                    referral_from = "Online"
                else:
                    referral = 1
                    referral_from = self.new_referral_txt_var.get()

                # re-create params for sql
                create_params = (
                    next_booking_id,
                    cus_acc,
                    garage_id,
                    vehicle_id,
                    referral,
                    referral_from,
                    package_id,
                    booking_date_str
                )

            # enact sql scripts
            for i, sql in enumerate(sql_statements):
            
                # create booking
                if i == 7 and not result:
                    conn.insert(sql, create_params)

            messagebox.showinfo("Booking", f"Thank you. Completed booking")

            # commit & close
            conn.close(True)

            self.load_table_data()

            return True, None

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            messagebox.showerror("Error", f"Failed to update booking:\n{err}")
            if conn:
                conn.close()
            else:
                pass
            return False, err

    def exist_booking_actions(self, action: str) -> tuple[bool, str | None]:
        """
        Docstring for exist_booking_actions
        
        :param self: pull from self params/funcs
        :param action: input string, edit or cancel actions support
        :type action: str
        :return: True for succes / False for fail. List of errors (or empty list)
        :rtype: tuple [bool, str | None]
        """
        # Ensure a row was selected
        if not hasattr(self, "selected_booking_ref"):
            messagebox.showwarning("No row selected", "Please select a booking to update.")
            return

        try:
            conn = None
           
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts (3 total)
            for i, sql in enumerate(sql_statements):

                # update existing booking
                if i == 4 and action in ['edit','cancel']:

                    # Build SQL update query            
                    params = (                
                        self.date_booking_var.get(),
                        self.car_reg_var.get(),
                        self.selected_booking_ref
                    )

                    result = self.check_user_inputs_edit(params)

                    # check if inputs are correct
                    if not result:

                        # update param with veh_id & reformat date
                        booking_date = datetime.strptime(self.date_booking_var.get(), "%d/%m/%Y")
                        booking_date_str = booking_date.strftime("%Y-%m-%d")

                        params = (
                            booking_date_str,
                            self.edi_veh_id,
                            self.selected_booking_ref
                            )   

                        # complete edit, else run cancel
                        if action == 'edit':

                            # update db
                            conn.update(sql, params)

                    else:
                        # pass error back to user/print
                        raise ValueError(result)

                # update existing booking
                if i == 6 and action == "cancel":
                    
                    # update db
                    conn.update(sql, (self.selected_booking_ref,))


            messagebox.showinfo("Saved", "Booking updated successfully.")
            
            # close & commit
            conn.close(True)

            # reset var
            self.edi_veh_id = None

            # Reload table
            self.load_table_data()

            return True, None

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            messagebox.showerror("Error", f"Failed to update booking:\n{err}")
            if conn:
                conn.close()
            else:
                pass
            return False, err
        
    def check_user_inputs_edit(self, data_list: list, cancel=False) -> list:
        """
        Docstring for check_user_inputs_edit
        
        :param self: pull from self params/funcs
        :param data_list: Input userparam list: [date_booking_var,car_reg_var,selected_booking_ref]
        :type data_list: list
        :param cancel: input default = false, True means don't check date past (as cancel requested)
        :type cancel: bool (default false)
        :return: List of errors (or empty list). Based on userchecks
        :rtype: list
        """
        output_msg = []

        # check if data input str               
        for i, data in enumerate(data_list):

            # check if none value
            if data is None or data == "":
                output_msg.append(f'{data}: Is missing input values')

        # validate format dd/MM/yyyy
        if not self.is_valid_date(data_list[0]):
            output_msg.append('Date Format should be dd/MM/yyyy')
        else:
            input_date = datetime.strptime(data_list[0], '%d/%m/%Y').date()

            # check only if cancel = True
            if cancel and date.today() > input_date:
                output_msg.append('Date is in the past')

        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("vehicle_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts
        for i, sql in enumerate(sql_statements):

            # get vehicle info
            if i == 5:
                all_veh_data = conn.query(sql, (self.curr_user,))

        # strip & trim value to check
        temp_veh_reg = data_list[1]        
        veh_ref = temp_veh_reg.strip().replace(" ", "")
        exist = False
        activeflag = False

        # check if veh in veh_list
        if all_veh_data[1]:
            for i, data in enumerate(all_veh_data[1]): 

                # check if reg exists
                if veh_ref in data[1]:
                    exist = True
                    self.edi_veh_id = data[0]

                # check if reg is active
                if 1 == data[4]:
                    activeflag = True

        else:
            output_msg.append(f"No Vechicles registered with application")

        # check if Vechicle is Active/Inactive
        if not activeflag:
            output_msg.append(f"Vechicle Inactive")

        # check if Vechicle Exists
        if not exist:
            output_msg.append(f"Vechicle Reg not found within APP, please check input")

        return output_msg
        
    def check_user_inputs_create(self, data_list: list) -> list:
        """
        Docstring for check_user_inputs_create
        
        :param self: pull from self params/funcs
        :param data_list: Input userparam list: [date_booking_var,car_reg_var,selected_booking_ref]
        :type data_list: list
        :return: List of errors (or empty list). Based on userchecks
        :rtype: list
        """
        output_msg = []

        # check if data input str               
        for i, data in enumerate(data_list):

            # check if none value
            if data is None or data == "":
                output_msg.append(f'Missing input values')

        # check if date format dd/MM/yyyy >= today
        result = self.is_valid_date(data_list[0])
        if not result:
            output_msg.append(f'Date Format should be dd/MM/yyyy')

        fdate = date.today()
        input_date = datetime.strptime(data_list[0], '%d/%m/%Y').date()
        if fdate > input_date:
            output_msg.append(f'Date is in the past')

        return output_msg

    def is_valid_date(self, date_str):
        """
        Check if date_str is in dd/MM/yyyy format.
        Returns True if valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def structure_frame(self):      
        """
        Docstring for structure_frame
        Not a function: a display of the structure of the frame visually to keep clear the 
                        relationships between the frames
        :param self: Description
        """

        """Tab2
        │
        ├── Label: Instructions
        └── Frame: self.frame  (main container)
            │
            ├── LabelFrame: booking_data_user_form ("Booking Information")
            │   ├── Frame: table_frame (row 0, col 0)
            │   │   ├── Treeview: self.tree 
            │   │   ├── Vertical Scrollbar (right side)
            │   │   └── Horizontal Scrollbar (bottom)
            │   │
            │   └── Frame: fields_frame
            │       └── Labels + Entry widgets (row 1, col 0)
            │           ├─ Update/Edit Bookings (row 1, col(s) 1-3)
            │           ├─ Login Name: Label
            │           ├─ ... 
            │           └─ Button: "Save Changes"
            │        
            │       
            │
            └── Button: "Close Application"
            """

    def normalise_date(self, date_str) -> str:
        """
        Docstring for normalise_date
        
        :param self: change '%d/%m/%Y', '%d/%m/%y' > ensure all are dd/MM/yyyy
        :param date_str: Str of date
        """

        for fmt in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%d/%m/%Y')
            
            except ValueError:
                pass

        raise ValueError('Invalid date format')