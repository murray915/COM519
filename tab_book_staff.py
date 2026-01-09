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
        self.prime_garage = uf.validate_primary_garage_id(curr_user, True)
        
        self.tab_name = "Complete Bookings"
        self.controller = controller
        self.booking_complete_status = '-'
        
        ttk.Label(self, text="This is the Booking Completion Tab" \
        "\n This booking table is populated based on the user (staff), primary garage. To view other garages, please update user account's primary garage" \
        "\n>To change the date of a booking, update the date in the box (from today onwards), and press 'Change Booking Date'."
        "\n>To Cancel the booking, press the 'Cancel Booking' button, this will close the booking."
        "\n>To Complete the booking, Update the payment Method (if required, to 'cash' or 'membership'), then add the Net, Vat and Gross totals and press the 'Complete Booking' button, this will close the booking completing the transaction."
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
                "Garage ID", "Garage Name", "Booking Ref", "Date of Booking",
                "Customer Vechicle Reg", "Package", "Items Consumed", "Payment Method",
                "Status", "Total Paid (Exc VAT)", "Total VAT", "Total Paid (Inc VAT)"
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
        fields_frame = tk.Frame(booking_data_staff_form)
        fields_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # config label & entry columns within frame
        fields_frame.grid_columnconfigure(0, weight=0) 
        fields_frame.grid_columnconfigure(1, weight=0) 

        # entrees
        # for edit/cancel 
        self.garage_ID_var                = tk.StringVar()
        self.garage_name_var              = tk.StringVar()
        self.booking_ref_var              = tk.StringVar()
        self.date_of_booking_var          = tk.StringVar()
        self.customer_vechicle_reg_var    = tk.StringVar()
        self.Package_var                  = tk.StringVar()
        self.items_consumed_var           = tk.StringVar()
        self.paymentmethod_var            = tk.StringVar()
        self.status_var                   = tk.StringVar()
        self.total_net_var                = tk.StringVar()
        self.total_VAT_var                = tk.StringVar()
        self.total_gross_var              = tk.StringVar()
        self.booking_complete_status_var  = tk.StringVar()

        # label params
        # for edit/cancel
        labels = [
                "Garage ID :", "Garage Name :", "Booking Ref :", "Date of Booking :",
                "Customer Vechicle Reg :", "Package :", "Items Consumed :", "Payment Method :",
                "Status :", "Total Paid (Exc VAT) :", "Total VAT :", "Total Paid (Inc VAT) :"
        ]

        # set fields to be edit/non-edit
        # for edit/cancel
        NO_ENTRY_FIELDS = {0, 1, 2, 4, 5, 6, 8}

        # vars
        # for edit/cancel
        vars = [
            self.garage_ID_var,self.garage_name_var,self.booking_ref_var,
            self.date_of_booking_var,self.customer_vechicle_reg_var,self.Package_var,
            self.items_consumed_var,self.paymentmethod_var,self.status_var,
            self.total_net_var,self.total_VAT_var,self.total_gross_var
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

        # buttons
        ttk.Button(fields_frame,text="Change Booking Date",command=lambda: self.exist_booking_actions("edit")).grid(row=5, column=3, columnspan=2, pady=10)
        ttk.Button(fields_frame,text="Cancel Booking",command=lambda: self.exist_booking_actions("cancel")).grid(row=9, column=3, columnspan=2, pady=10)
        
        tk.Label(fields_frame, textvariable=self.booking_complete_status_var).grid(row=14, column=3, sticky="w")
        ttk.Button(fields_frame,text="Complete Booking",command=self.complete_booking).grid(row=15, column=3, columnspan=2, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        return booking_data_staff_form
    
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
            sql = uf.load_sql_file("booking_staff_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next transaction id
                if i == 1:
                    next_transaction_id = conn.query(sql, ())
                    next_transaction_id = next_transaction_id[1][0][0]

                # get table data
                # current open bookings
                if i == 0:
                    rows = conn.query(sql, (self.prime_garage,))

                    # check for return data
                    if rows:
                        headers = rows[0]         # headers from sql
                        data_rows = rows[1]       # data from sql, list of rows

                        for row in data_rows: # get data by row
                            self.tree.insert("", "end", values=row)
                                # get part_names, for package info dropdown results

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

        self.garage_ID_var.set(values[0])
        self.garage_name_var.set(values[1])
        self.booking_ref_var.set(values[2])
        self.date_of_booking_var.set(values[3])
        self.customer_vechicle_reg_var.set(values[4])
        self.Package_var.set(values[5])
        self.items_consumed_var.set(values[6])
        self.paymentmethod_var.set(values[7])
        self.status_var.set(values[8])
        self.total_net_var.set(values[9])
        self.total_VAT_var.set(values[10])
        self.total_gross_var.set(values[11])

        self.selected_booking_ref = values[2]

        self.get_booking_completion_check()
        self.booking_complete_status_var.set(self.booking_complete_status)

    def on_show(self):
        """Called whenever this tab becomes active"""
        print("Refreshing Tab data")
        self.prime_garage = uf.validate_primary_garage_id(self.curr_user, True)
        self.load_table_data()

    def get_booking_completion_check(self):

        conn = None
        stock_stock_check = True
        qtys_per_item = []
        stock_check_dict = {}
        outmsg = []

        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("booking_staff_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get item_id list from booking
            if i == 5:
                
                data = conn.query(sql, (self.booking_ref_var.get(),))

                # check for N/A on items consumed
                if data[1][0][0] == 'N/A':
                    
                    # no stock update required
                    stock_stock_check = False

                else:
                    # cleanup returned data list > str of itm refs
                    data_str_item_comsumed = data[1][0][0]
                    data_str_item_QTY_comsumed = data[1][0][1]
                    self.booking_veh = data[1][0][2]

                    # cleanup data into string values
                    cleaned_data = data_str_item_comsumed.replace("[","").replace("]","").split(",")
                    self.part_number_list = cleaned_data
                    final_data = ",".join(f"'{item}'" for item in cleaned_data)
                    qtys_per_item = data_str_item_QTY_comsumed.split(",")
                    self.part_number_qty_list = qtys_per_item

            # get the stock levels for items and garage (if items are within package)
            if i == 6 and stock_stock_check:
                
                # search params
                # garage id formatting for db
                garage_id = self.garage_ID_var.get().replace("-","_")
                sql_garage_id = f'stocklevel_{garage_id}'
                sql = sql.replace("replace1", sql_garage_id)

                # update sql with part_id in list values
                sql = sql.replace("replace2",final_data)

                # get stock QTY for garage by item
                data = conn.query(sql, ())

                # setup dictionary for item & qty current stock levels
                self.curr_stock_level_dict = {}
                for i, key in enumerate(data[1]):
                    self.curr_stock_level_dict[key[0]] = int(key[1])

                # setup dictionary for qty check
                for i, key in enumerate(cleaned_data):
                    stock_check_dict[key] = int(qtys_per_item[i])

                # cycle through items against dictionary
                for i in data[1]:

                    stock_level = stock_check_dict[i[0]]

                    # check in dict of stocks if current level is sufficient
                    if stock_level > i[1]:
                        outmsg.append(f"Stock for {i[0]} is insufficient to complete booking")

                # add stock checks to var if fails found
                if not outmsg:
                    self.booking_complete_status = 'Sufficient stock to Complete'
                else:
                    self.booking_complete_status = ",".join(outmsg)
        
        conn.close()

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
            sql = uf.load_sql_file("booking_staff_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts (3 total)
            for i, sql in enumerate(sql_statements):

                # update existing booking
                if i == 2 and action in ['edit','cancel']:

                    # Build SQL update query
                    fixed_date = self.normalise_date(self.date_of_booking_var.get())        
                    params = (
                        fixed_date
                    )

                    result = self.check_user_inputs_edit(params, False)

                    # check if inputs are correct
                    if not result:

                        # update param with veh_id & reformat date
                        booking_date = datetime.strptime(self.date_of_booking_var.get(), "%d/%m/%Y")
                        booking_date_str = booking_date.strftime("%Y-%m-%d")

                        params = (
                            booking_date_str,
                            self.selected_booking_ref
                            )   

                        # complete edit, else run cancel
                        if action == 'edit':

                            # update db
                            conn.update(sql, params)

                            # cleanup 
                            self.garage_ID_var.set('')
                            self.garage_name_var.set('')
                            self.booking_ref_var.set('')
                            self.date_of_booking_var.set('')
                            self.customer_vechicle_reg_var.set('')
                            self.Package_var.set('')
                            self.items_consumed_var.set('')
                            self.paymentmethod_var.set('')
                            self.status_var.set('')
                            self.total_net_var.set('')
                            self.total_VAT_var.set('')
                            self.total_gross_var.set('')

                    else:
                        # pass error back to user/print
                        raise ValueError(result)

                # update existing booking
                if i == 3 and action == "cancel":
                    
                    # update db
                    conn.update(sql, (self.selected_booking_ref,))

                    # cleanup 
                    self.garage_ID_var.set('')
                    self.garage_name_var.set('')
                    self.booking_ref_var.set('')
                    self.date_of_booking_var.set('')
                    self.customer_vechicle_reg_var.set('')
                    self.Package_var.set('')
                    self.items_consumed_var.set('')
                    self.paymentmethod_var.set('')
                    self.status_var.set('')
                    self.total_net_var.set('')
                    self.total_VAT_var.set('')
                    self.total_gross_var.set('')

            messagebox.showinfo("Saved", "Booking updated successfully.")
            
            # close & commit
            conn.close(True)

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

    def complete_booking(self) -> tuple[bool, str | None]:
        """
        Docstring for exist_booking_actions
        
        :param self: pull from self params/funcs
        :return: True for succes / False for fail. List of errors (or empty list)
        :rtype: tuple [bool, str | None]
        """
        # Ensure a row was selected
        if not hasattr(self, "selected_booking_ref"):
            messagebox.showwarning("No row selected", "Please select a booking to update.")
            return

        try:
            conn = None
            sql_vars = []
            outmsg = []

            # check if stock levels are sufficient
            self.get_booking_completion_check()                   
            if self.booking_complete_status != 'Sufficient stock to Complete':
                outmsg.append("Stock Levels insufficient. Review required")

            # check payment method input valid
            pay_method = self.paymentmethod_var.get()
            if pay_method.lower() not in ["card","cash","membership"]:
                outmsg.append("Payment method needs to be cash/membership/card")

            var_list = [self.total_net_var.get().replace("£",""),self.total_VAT_var.get().replace("£",""),self.total_gross_var.get().replace("£","")]
            
            if self.validate_float_list(",".join(var_list)):
                # Convert once to floats
                net, vat, gross = [float(v) for v in var_list]

                # Check positive
                if net <= 0 or vat <= 0 or gross <= 0:
                    outmsg.append("Payment values Net/VAT/Gross must be positive (> £0)")

                # Check Net + VAT = Gross (allow small rounding error)
                elif abs((net + vat) - gross) > 0.001:
                    outmsg.append("Payment values Net + VAT do not equal Gross")
                    
            else:
                outmsg.append("Value input into one of the Payment Values (net/vat/gross) are not ")

            # if bad inputs, error and return to user
            if outmsg:
                #messagebox.showerror("Validation Error", "\n".join(outmsg))
                raise ValueError(outmsg)

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("booking_staff_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts (3 total)
            for i, sql in enumerate(sql_statements):
                
                # get next id
                if i == 1:

                    # get next id
                    data = conn.query(sql, ())
                    self.next_transaction_id = data[1][0][0]

                    # generate the transaction VALUES for sql
                    for i, _ in enumerate(self.part_number_list):

                        # get item & QTY consumed
                        item_ref = self.part_number_list[i]
                        qty_consumed = self.part_number_qty_list[i]
                        
                        # collect sql update VALUES
                        sql_vars.append((                            
                            self.booking_ref_var.get(),
                            self.booking_veh,
                            item_ref,
                            int(qty_consumed)                            
                        ))

                    # update sql_vars > tuple list for sql inc. transaction ID increasing
                    start_index = int(self.next_transaction_id[-3:])
                    sql_params = []
                    for i, row in enumerate(sql_vars):
                        tact_number = f"TACT-{start_index + i:03d}"
                        sql_params.append((tact_number,) + row)

                # update booking with values & paid complete
                if i == 7:

                    sql_values = [net, vat, gross,self.booking_ref_var.get()]
                    conn.update(sql, sql_values)

                # insert into transactions table
                if i == 8:

                    values_str = ", ".join(
                        str(t) for t in sql_params
                    )

                    sql = sql.replace("replace",values_str)
                    conn.insert(sql, ())

                # update stock levels
                if i == 9:

                    # get garage_id for sql
                    garage_id = self.garage_ID_var.get().replace("-","_")
                    sql_garage_id = f'stocklevel_{garage_id}'
                    sql = sql.replace("replace", sql_garage_id)

                    # update each item for transaction records
                    for i, item in enumerate(self.part_number_list):

                        # get current stock
                        curr_stock_level = self.curr_stock_level_dict[item]

                        # get item & qty params
                        item_ref = self.part_number_list[i]
                        qty_consumed = self.part_number_qty_list[i]

                        # cal new stock level
                        new_stock_level = int(curr_stock_level) - int(qty_consumed)

                        # update db
                        conn.update(sql, (int(new_stock_level),item_ref))

                    # cleanup 
                    self.garage_ID_var.set('')
                    self.garage_name_var.set('')
                    self.booking_ref_var.set('')
                    self.date_of_booking_var.set('')
                    self.customer_vechicle_reg_var.set('')
                    self.Package_var.set('')
                    self.items_consumed_var.set('')
                    self.paymentmethod_var.set('')
                    self.status_var.set('')
                    self.total_net_var.set('')
                    self.total_VAT_var.set('')
                    self.total_gross_var.set('')


            messagebox.showinfo("Info", "Booking Completed successfully.")

            # close & commit
            conn.close(True)

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

    def validate_float_list(self, input_str: str) -> bool:
        """
        Check if input_str is a comma-separated list of floats.

        :param input_str: string input like "1,2,3"
        :return: True if valid, False otherwise
        """
        try:
            # Split by comma
            parts = input_str.split(",")

            # Check each part is an float
            for part in parts:
                float(part)  # raises ValueError if not an float

            return True
        except ValueError:
            return False

    def check_user_inputs_edit(self, data_list: str, cancel=False) -> list:
        """
        Docstring for check_user_inputs_edit
        
        :param self: pull from self params/funcs
        :param data_list: Input userparam str: date_booking_var
        :type data_list: str
        :param cancel: input default = false, True means don't check date past (as cancel requested)
        :type cancel: bool (default false)
        :return: List of errors (or empty list). Based on userchecks
        :rtype: list
        """
        output_msg = []

        # check if data input str               
        if data_list is None or data_list == '':
            output_msg.append('Missing Date input')

        # validate format dd/MM/yyyy
        if not self.is_valid_date(data_list):
            output_msg.append('Date Format should be dd/MM/yyyy')
        else:
            input_date = datetime.strptime(data_list, '%d/%m/%Y').date()

            # check only if cancel = True
            if not cancel and date.today() > input_date:
                output_msg.append('Date is in the past')

        return output_msg

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