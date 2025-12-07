import tkinter as tk
import icecream as ic
import utility_functions as uf
import image_functions as ifc
import registration_window as rg
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Tab5(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "My Account"
        self.controller = controller

        self.name = '-'
        self.address = '-'
        self.postcode = '-'
        self.postcode_id = '-'
        self.email = '-'
        self.phone_no = '-'
        self.primary_gar = '-'
        self.access_code = '-'
        self.active_flag = '-'

        self.customer_veh_id = '-'
        self.car_reg = '-'
        self.car_make = '-'
        self.car_model = '-'
        self.mot_status = '-'
        self.veh_active_flag = '-'
        self.veh_list = '-'

        self.customer_ref = uf.validate_customer_account(self.curr_user, False)

        ttk.Label(self, text="This is the Account Management Tab" \
        "\n> To change account details, including password. Please update the required fields and press the 'Update my details' button." \
        "\n> To update password, please input current password and then your new password (in both the first and second box), then 'Update my password', button." \
        "\n> To deactivate your account completely. Please tick the deactivation box, and input username and password. This will complete the process and close the application & deactivate your account. To reactivate, please untick the box when updating" \
        
        "\n\n> To add a new vehicle to your account, please within the 'Vehicle Information' window, add the details to the 4 boxes and press the 'Update/Add vehicle' button." \
        "\n> To update a vehicle, please select one vehicle from the dropdown box, update respective fields, and press'Update/Add vehicle' button. To deactivate a vehicle, check box to deactivate and press 'update my vehicle list', to reactivate, when updating untick the box."
        "\n\n> To add a membership, please ..."
        ).pack(pady=20)

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Account Info
        # row 0, col 0
        self.account_info_frame = self.frame_1()

        # frame 2 - Item Creation
        # row 0, col 5
        self.account_vehicle_frame = self.frame_2()

        # frame 3 - Item Image Upload
        # row 1, col 5
        #self.item_comsumption_graph_frame = self.frame_3()


        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)


    def frame_1(self) -> object:
        """
        constructor for frame 1 : account_info_frame
        """

        account_info_frame = tk.LabelFrame(self.frame, text="Account Information")
        account_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
        # Labels
        self.name_var = tk.StringVar()
        tk.Label(account_info_frame, text="Name").grid(row=1, column=0)
        self.name_entry = tk.Entry(account_info_frame, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=1, column=1, columnspan=3, sticky="we")

        self.address_var = tk.StringVar()
        tk.Label(account_info_frame, text="Address").grid(row=2, column=0)
        self.address_entry = tk.Entry(account_info_frame, textvariable=self.address_var, width=40)
        self.address_entry.grid(row=2, column=1, columnspan=3, sticky="we")

        self.postcode_var = tk.StringVar()
        tk.Label(account_info_frame, text="Postcode").grid(row=3, column=0)
        self.postcode_entry = tk.Entry(account_info_frame, textvariable=self.postcode_var, width=40)
        self.postcode_entry.grid(row=3, column=1, columnspan=3, sticky="we")

        self.email_var = tk.StringVar()
        tk.Label(account_info_frame, text="Email").grid(row=4, column=0)
        self.email_entry = tk.Entry(account_info_frame, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=4, column=1, columnspan=3, sticky="we")

        self.phone_no_var = tk.StringVar()
        tk.Label(account_info_frame, text="Phone Number").grid(row=5, column=0)
        self.phone_no_entry = tk.Entry(account_info_frame, textvariable=self.phone_no_var, width=40)
        self.phone_no_entry.grid(row=5, column=1, columnspan=3, sticky="we")

        self.primary_gar_var = tk.StringVar()
        tk.Label(account_info_frame, text="Primary Garage").grid(row=6, column=0)
        self.primary_gar_entry = tk.Entry(account_info_frame, textvariable=self.primary_gar_var, width=40)
        self.primary_gar_entry.grid(row=6, column=1, columnspan=3, sticky="we")

        self.access_code_var = tk.StringVar()
        self.active_flag_var = tk.StringVar()

        # entrys / combobox
        update_user_data = tk.Button(account_info_frame,text='Update User Data',command=lambda: self.get_user_info(True))
        update_user_data.grid(row=1, column=4)
        
        self.get_user_info(False)

        # format frame widgets
        for widget in account_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return account_info_frame
    
    def frame_2(self):
        """
        constructor for frame 2 : account_vehicle_frame
        """

        account_vehicle_frame = tk.LabelFrame(self.frame, text="Vehicle Information")
        account_vehicle_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
 
        # Labels
        tk.Label(account_vehicle_frame, text="Dropdown List for Vehicles :").grid(row=0, column=0)

        self.customer_veh_id_var = tk.StringVar(value=self.customer_veh_id)
        tk.Label(account_vehicle_frame, text="Vehicle ID").grid(row=1, column=0)
        tk.Label(account_vehicle_frame, textvariable=self.customer_veh_id_var).grid(row=1, column=1)

        self.active_flag_veh_var = tk.StringVar(value=self.veh_active_flag)
        tk.Label(account_vehicle_frame, text="Active Status").grid(row=2, column=0)
        tk.Label(account_vehicle_frame, textvariable=self.active_flag_veh_var).grid(row=2, column=1)

        self.car_reg = tk.StringVar()
        tk.Label(account_vehicle_frame, text="Registration No.").grid(row=3, column=0)
        self.car_reg_entry = tk.Entry(account_vehicle_frame, textvariable=self.car_reg, width=40)
        self.car_reg_entry.grid(row=3, column=1, columnspan=3, sticky="we")

        self.car_make_var = tk.StringVar()
        tk.Label(account_vehicle_frame, text="Vehicle Make").grid(row=4, column=0)
        self.car_make_entry = tk.Entry(account_vehicle_frame, textvariable=self.car_make_var, width=40)
        self.car_make_entry.grid(row=4, column=1, columnspan=4, sticky="we")

        self.car_model_var = tk.StringVar()
        tk.Label(account_vehicle_frame, text="Vehicle Model").grid(row=5, column=0)
        self.car_model_entry = tk.Entry(account_vehicle_frame, textvariable=self.car_model_var, width=40)
        self.car_model_entry.grid(row=5, column=1, columnspan=4, sticky="we")

        self.mot_status_var = tk.StringVar()
        tk.Label(account_vehicle_frame, text="MOT Status").grid(row=6, column=0)
        self.mot_status_entry = tk.Entry(account_vehicle_frame, textvariable=self.mot_status_var, width=40)
        self.mot_status_entry.grid(row=6, column=1, columnspan=3, sticky="we")

        # entrys / combobox
        self.veh_combobox = ttk.Combobox(account_vehicle_frame, values=self.veh_list)
        self.veh_combobox.grid(row=0, column=1, columnspan=3, sticky="ew")
        
        self.checK_veh_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(account_vehicle_frame, text="De-activate Vehicle?", variable=self.checK_veh_var)
        self.checkbox.grid(row=2, column=4)

        veh_get_data = tk.Button(account_vehicle_frame,text='Get Vehicle Data',command=lambda: self.get_veh_info(False, False))
        veh_get_data.grid(row=0, column=4)

        veh_clear_data = tk.Button(account_vehicle_frame,text='Clear Input Vehicle Data',command=self.clear_inputs)
        veh_clear_data.grid(row=1, column=4)

        update_veh_data = tk.Button(account_vehicle_frame,text='Update / Add Vehicle Data',command=lambda: self.get_veh_info(True, False))
        update_veh_data.grid(row=6, column=4)

        self.get_veh_info(False, False)

        # format frame widgets
        for widget in account_vehicle_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return account_vehicle_frame


    def get_veh_info(self, update:bool, create: bool) -> tuple[bool, str | None]:
        """
        get_veh_info from curr_user passed into class

        :param self: self, pulled on setup & update details, update trigger from button pressed by user to update details
        :return: True is successful, or false and errorstring
        :rtype: tuple[bool, str | None]
        """

        try:
            conn = None

            # get the part_id from search/selector
            dropdown_checker = self.veh_combobox.get()

            if dropdown_checker != '':
                self.customer_veh_id = dropdown_checker[0:10]

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("vehicle_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next id
                if i == 0:
                    veh_id = conn.query(sql, ())
                    next_veh_id = veh_id[1][0][0]

                # get vehicle info for dropdown
                if i == 1:
                    all_veh_data = conn.query(sql, (self.customer_ref,))

                    if all_veh_data:
                        output_list = []

                        # clean data intp list
                        for i in all_veh_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.veh_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.veh_combobox['values'] = self.veh_list
                    self.veh_combobox.set('')

                # get vehicle info data
                if i == 2 and dropdown_checker != '':
                    veh_info = conn.query(sql, (self.customer_veh_id,))
                
                    # remove existing data
                    self.customer_veh_id_var.set('-')
                    self.car_reg_entry.delete(0, tk.END)
                    self.car_make_entry.delete(0, tk.END)
                    self.car_model_entry.delete(0, tk.END)
                    self.mot_status_entry.delete(0, tk.END)
                    self.active_flag_var.set('-')

                    # if data found for search/item selector, update self data
                    if veh_info[1]:
                        rows = veh_info[1]

                        if rows:
                            (
                                veh_id,
                                cus_id,
                                car_reg,
                                car_make,
                                car_model,
                                mot_status,
                                active_flag
                            ) = rows[0]

                            # add details to entry & save others to var

                            self.customer_veh_id_var.set(veh_id)
                            self.car_reg_entry.insert(0, car_reg)
                            self.car_make_entry.insert(0, car_make)
                            self.car_model_entry.insert(0, car_model)
                            self.mot_status_entry.insert(0, mot_status)

                        # convert bool to text value & update checkbox
                        if active_flag == 1:
                            self.active_flag_veh_var.set("Active")
                            self.checK_veh_var.set(False)
                        elif active_flag == 0:
                            self.active_flag_veh_var.set("Inactive")
                            self.checK_veh_var.set(True)

                # update user details
                if i == 3 and update:
                    
                    # get user inputs
                    deactivate_flag = self.checK_veh_var.get()

                    # if tickbox = False, active
                    if deactivate_flag:
                        active_status = 0
                    elif not deactivate_flag:
                        active_status = 1

                    veh_id = str(self.customer_veh_id_var.get())
                    car_ref = str(self.car_reg_entry.get())
                    car_make = str(self.car_make_entry.get())
                    car_model = str(self.car_model_entry.get())
                    car_status = str(self.mot_status_entry.get())

                    variable_list = (veh_id, car_ref, car_make, car_model, car_status)

                    # check for user inputs into all boxes
                    # any missing values error to user
                    if any(not var for var in variable_list):
                        messagebox.showerror("Show Error","Please ensure all boxes are populated.")
                        raise ValueError("Missing data within inputs")
                  
                    conn.update(sql, (car_ref,car_make,car_model,car_status, active_status, veh_id))


                    messagebox.showinfo("Show Info",f"Vehicle Details updated")
                    
                    # remove existing data
                    self.customer_veh_id_var.set('-')
                    self.car_reg_entry.delete(0, tk.END)
                    self.car_make_entry.delete(0, tk.END)
                    self.car_model_entry.delete(0, tk.END)
                    self.mot_status_entry.delete(0, tk.END)
                    self.active_flag_veh_var.set('-')
                    self.checK_veh_var.set(False)
                  


            # commit & close
            conn.close(True)   

            # update dropdowns
            self.update_dropdown()

            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)


    def update_dropdown(self) -> tuple[bool, str | None]:
        """
        update dropdown combobox

        :param self: self, pulled on setup & update details, update trigger from button pressed by user to update details
        :return: True is successful, or false and errorstring
        :rtype: tuple[bool, str | None]
        """

        try:
            conn = None

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("vehicle_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get vehicle info for dropdown
                if i == 1:
                    all_veh_data = conn.query(sql, (self.customer_ref,))

                    if all_veh_data:
                        output_list = []

                        # clean data intp list
                        for i in all_veh_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.veh_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.veh_combobox['values'] = self.veh_list
                    self.veh_combobox.set('')
                  
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


    def get_user_info(self, update: bool) -> tuple[bool, str | None]:
        """
        get_user_info from curr_user passed into class

        :param self: self, update trigger from button pressed by user to update details
        :return: True is successful, or false and errorstring
        :rtype: tuple[bool, str | None]
        """

        try:
            conn = None

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("user_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get user info data
                if i == 1 and not update:
                    user_info = conn.query(sql, (self.curr_user,))
                
                    # remove existing data
                    self.name_entry.delete(0, tk.END)
                    self.address_entry.delete(0, tk.END)
                    self.postcode_entry.delete(0, tk.END)
                    self.email_entry.delete(0, tk.END)
                    self.phone_no_entry.delete(0, tk.END)
                    self.primary_gar_entry.delete(0, tk.END)

                    # if data found for search/item selector, update self data
                    if user_info[1]:
                        rows = user_info[1]

                        if rows:
                            (
                                user_id,
                                name,
                                address,
                                postcode,
                                email,
                                phoneno,
                                prime_gar,
                                access_code,
                                active_flag
                            ) = rows[0]

                            # add details to entry & save others to var
                            self.name_entry.insert(0, name)
                            self.address_entry.insert(0, address)
                            self.postcode_entry.insert(0, postcode)
                            self.email_entry.insert(0, email)
                            self.phone_no_entry.insert(0, phoneno)
                            self.primary_gar_entry.insert(0, prime_gar)
                            self.access_code_var.set(access_code)
                            self.active_flag_var.set(active_flag)

                        # convert bool to text value
                        if active_flag == 1:
                            self.access_code_var.set("Active")
                        elif active_flag == 0:
                            self.access_code_var.set("Inactive")

                        # get postcode_id
                        self.postcode_id = uf.validate_postcode(postcode, True)

                # update user details
                if i == 2 and update:
                    
                    result = self.check_user_inputs()

                    # update account if all inputs ok
                    if result:

                        # get user inputs
                        name = str(self.name_entry.get())
                        address = str(self.address_entry.get())
                        postcode = str(self.postcode_entry.get())
                        email = str(self.email_entry.get())
                        phoneno = str(self.phone_no_entry.get())
                        prime_gar = str(self.primary_gar_entry.get())

                        # get postcode_id (create new if required)
                        postcode_id = uf.validate_postcode(postcode, True)
                        
                        conn.update(sql, (name, address, postcode_id, email, phoneno, prime_gar, self.curr_user))

                        messagebox.showinfo("Show Info",f"Account Details updated")

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
        

    def check_user_inputs(self) -> tuple[bool, str | None]:
        """
        check user inputs for the edit acc boxes within frame 1
        Return True, or False for sucess with errorstring (where applic)
        """

        try:
            
            # get user input params
            name = str(self.name_entry.get())
            address = str(self.address_entry.get())
            postcode = str(self.postcode_entry.get())
            email = str(self.email_entry.get())
            phoneno = str(self.phone_no_entry.get())
            prime_gar = str(self.primary_gar_entry.get())

            variable_list = (name, address, postcode, email, phoneno, prime_gar)

            # check for user inputs into all boxes
            # any missing values error to user
            if any(not var for var in variable_list):
                messagebox.showerror("Show Error","Please ensure all boxes are populated. Only primary garage is not required, input 'N/A' for this.")
                raise ValueError("Missing data within inputs")
            
            # check only if phone number isn't an int
            cleaned_num = phoneno.replace(" ", "")
            if not cleaned_num.isdigit():  
                messagebox.showerror("Show Error",'Input for phone number is not a number, required is a number eg. 0123123123')
                raise ValueError("Input incorrect, not a string or 'N/A'")

            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")            
            return False, str(err)
        
    def clear_inputs(self):
        """
        clear inputs from frame 2
        """
        
        # remove existing data
        self.customer_veh_id_var.set('-')
        self.car_reg_entry.delete(0, tk.END)
        self.car_make_entry.delete(0, tk.END)
        self.car_model_entry.delete(0, tk.END)
        self.mot_status_entry.delete(0, tk.END)
        self.active_flag_veh_var.set('-')
        self.checK_veh_var.set(False)