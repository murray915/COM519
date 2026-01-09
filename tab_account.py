import tkinter as tk
import icecream as ic
import re
import utility_functions as uf
import image_functions as ifc
import registration_window as rg
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
from tkinter import PhotoImage, messagebox
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
        self.garge_list = '-'

        self.membership_id = '-'
        self.customer_id = '-'
        self.subscrip_dat = '-'
        self.payment_method = "Card"
        self.iban = '-'

        self.username = '-'
        self.image = None

        #encryption
        self.f_key = None
        self.get_key()

        self.customer_ref = uf.validate_customer_account(self.curr_user, False)

        ttk.Label(self, text="This is the Account Management Tab" \
        "\nAccount information box" \
        "\n> To change your name, address, contact details or primary garage, please edit the required fields then click the 'Update my details' button." \
        "\nVehicle information box"
        "\n> To add a new vehicle to your account, please add the details to the four boxes and press the 'Add vehicle data' button. MOT status = 'pass' or 'fail'" \
        "\n> To update a vehicle, please select one vehicle from the dropdown menu, update respective fields, and press'Update vehicle data' button. " \
        "\n> To deactivate a vehicle, select one vehicle from the dropdown menu, check box to deactivate then press 'update vehicle data' To reactivate, when updating untick the box." \
        "\nMembership information box" \
        "\n> To create a membership, input Iban and day for payment then press 'Create/Update Details'. " \
        "\n> To update a membership, edit the data displayed and press the 'Create/Update Details'." \
        "\n> To deactivate a membership, press the 'Deactivate my membership' button."
        "\nPassword reset box"
        "\n> To update password, please input current password in the first box and then your new password in both the second and third boxes, then press 'Update password', button." 
        
        ).pack(pady=20)

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Account Info
        # row 0, col 0
        self.account_info_frame = self.frame_1()

        # frame 2 - Vehicle Details (Edit/Add)
        # row 1, col 0
        self.account_vehicle_frame = self.frame_2()

        # frame 3 - Password Reset
        # row 1, col 4
        self.password_reset_frame = self.frame_3()

        # frame 4 - Image
        # row 0, col 4
        self.image_frame = self.frame_4()

        # frame 5 - Membership
        # row 0, col 4
        self.membership_frame = self.frame_5()

        # get data for frames
        result = self.get_user_info(False)

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
        garage_list_details = tk.Button(account_info_frame,text='Garage List',command=self.get_garagelist_details)
        garage_list_details.grid(row=6, column=4)

        update_user_data = tk.Button(account_info_frame,text='Update User Data',command=lambda: self.get_user_info(True))
        update_user_data.grid(row=1, column=4)
        
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

        update_veh_data = tk.Button(account_vehicle_frame,text='Update Vehicle Data',command=lambda: self.get_veh_info(True, False))
        update_veh_data.grid(row=6, column=4)

        create_veh_data = tk.Button(account_vehicle_frame,text='Add Vehicle Data',command=lambda: self.get_veh_info(False, True))
        create_veh_data.grid(row=6, column=5)

        self.get_veh_info(False, False)

        # format frame widgets
        for widget in account_vehicle_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return account_vehicle_frame
   
    def frame_3(self):
        """
        constructor for frame 3 : password_reset_frame
        """

        password_reset_frame = tk.LabelFrame(self.frame, text="Password Reset")
        password_reset_frame.grid(row=1, column=3, padx=5, pady=5, sticky="nw")
 
        # Labels
        tk.Label(password_reset_frame, text="Please input Username, current password and new password (and re-enter) to update password").grid(row=0, column=0)

        self.username_var = tk.StringVar(value=self.username)
        tk.Label(password_reset_frame, text="username").grid(row=1, column=0)
        tk.Label(password_reset_frame, textvariable=self.username_var).grid(row=1, column=1)

        self.curr_pass_var = tk.StringVar()
        tk.Label(password_reset_frame, text="Current Password").grid(row=2, column=0)
        self.curr_pass_var_entry = tk.Entry(password_reset_frame, textvariable=self.curr_pass_var, show='*', width=40)
        self.curr_pass_var_entry.grid(row=2, column=1, columnspan=2, sticky="we")

        self.new_pass_1_var = tk.StringVar()
        tk.Label(password_reset_frame, text="New Password").grid(row=3, column=0)
        self.new_pass_1_entry = tk.Entry(password_reset_frame, textvariable=self.new_pass_1_var, show='*', width=40)
        self.new_pass_1_entry.grid(row=3, column=1, columnspan=2, sticky="we")

        self.new_pass_2_var = tk.StringVar()
        tk.Label(password_reset_frame, text="New Password (Re-enter)").grid(row=4, column=0)
        self.new_pass_2_entry = tk.Entry(password_reset_frame, textvariable=self.new_pass_2_var, show='*', width=40)
        self.new_pass_2_entry.grid(row=4, column=1, columnspan=2, sticky="we")

        # entrys / combobox
        update_pass_data = ttk.Button(password_reset_frame,text='Update Password',command=self.user_password_updater)
        update_pass_data.grid(row=6, column=1)

        pw_requirement_details = tk.Button(password_reset_frame,text='Password Requirements',command=self.pw_requirements_printout)
        pw_requirement_details.grid(row=6, column=0)

        # format frame widgets
        for widget in password_reset_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return password_reset_frame

    def frame_4(self):

        image_frame = tk.LabelFrame(self.frame, text=" - ")
        image_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
 
        # background image
        img = Image.open("./images/User_Icon.png")
        img = img.resize((120, 120))
        self.image = ImageTk.PhotoImage(img)

        #self.image = PhotoImage(file="./images/User_Icon.png")
        tk.Label(image_frame, image=self.image).grid(row=0, column=3, rowspan=3, padx=10, pady=10)

    def frame_5(self):
        """
        constructor for frame 5 : membership_frame
        """

        membership_frame = tk.LabelFrame(self.frame, text="Membership Information")
        membership_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
 
        # Labels
        self.membership_id_var = tk.StringVar(value=self.membership_id)
        tk.Label(membership_frame, text="Membership ID").grid(row=0, column=0)
        tk.Label(membership_frame, textvariable=self.membership_id_var).grid(row=0, column=1)

        self.customer_id_var = tk.StringVar(value=self.customer_id)
        tk.Label(membership_frame, text="Customer ID").grid(row=1, column=0)
        tk.Label(membership_frame, textvariable=self.customer_id_var).grid(row=1, column=1)

        self.subscrip_dat_var = tk.StringVar()
        tk.Label(membership_frame, text="Subscription Payment Day (input 1-25th to denote the day)").grid(row=2, column=0)
        self.subscrip_dat_entry = tk.Entry(membership_frame, textvariable=self.subscrip_dat_var, width=40)
        self.subscrip_dat_entry.grid(row=2, column=1, columnspan=2, sticky="we")

        self.payment_method_var = tk.StringVar(value=self.payment_method)
        tk.Label(membership_frame, text="Payment Method").grid(row=3, column=0)
        tk.Label(membership_frame, textvariable=self.payment_method_var).grid(row=3, column=1)

        self.iban_var = tk.StringVar()
        tk.Label(membership_frame, text="Iban").grid(row=4, column=0)
        self.iban_entry = tk.Entry(membership_frame, textvariable=self.iban_var, width=40)
        self.iban_entry.grid(row=4, column=1, columnspan=2, sticky="we")

        # entrys / combobox
        update_veh_data = tk.Button(membership_frame,text='Create/Update Details',command=lambda: self.get_membership_info(True, False))
        update_veh_data.grid(row=0, column=2)

        update_veh_data = tk.Button(membership_frame,text='Deactivate my membership',command=lambda: self.get_membership_info(False, True))
        update_veh_data.grid(row=1, column=2)

        # format frame widgets
        for widget in membership_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return membership_frame

    def on_show(self):
        """Called whenever this tab becomes active"""
        print("Refreshing Tab data")
        self.get_user_info(False)

    def get_membership_info(self, action:bool, delete: bool) -> tuple[bool, str | None]:
        """
        get_membership_info from existing params. Update and create where button input

        :param self: self, pulled on setup & update details, update trigger from button pressed by user to update details. delete trigger from button to deactivate membership
        :return: True is successful, or false and errorstring
        :rtype: tuple[bool, str | None]
        """

        try:
            # var setups
            conn = None
            create = False
            update = False

            # confirm if update/create
            member_id = self.membership_id_var.get()
            if action and member_id != 'None':
                update = True
            if action and member_id == 'None':
                create = True

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("membership_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next id
                if i == 0:
                    next_mem_id = conn.query(sql, ())
                    next_mem_id = next_mem_id[1][0][0]

                # get account data, check inputs
                # update if required
                if i == 1 and action:

                    # get and validate data
                    membership_id = self.membership_id
                    if membership_id is None:
                        membership_id = "Nothing"

                    customer_id = self.customer_id
                    if customer_id is None:
                        customer_id = "Nothing"

                    subscrip_pay_day = self.subscrip_dat_entry.get()
                    pay_method = "Card"
                    iban = self.iban_entry.get()

                    var_list = [
                        customer_id,
                        str(subscrip_pay_day),
                        pay_method,
                        str(iban),
                        membership_id
                    ]

                    # check for user inputs into all boxes
                    # any missing values error to user
                    if any(not var for var in var_list):
                        messagebox.showerror("Show Error","Please ensure all boxes are populated. Only primary garage is not required, input 'N/A' for this.")
                        raise ValueError("Missing data within inputs")
                    
                    if not subscrip_pay_day.isdigit() or not (1 <= int(subscrip_pay_day) <= 25):
                        messagebox.showerror("Show Error","Please ensure Day input into pay day is a number between 1-25.")
                        raise ValueError("Data input incorrect for day input, should be 1-25")
                    
                    # update record, otherwise create new
                    if update:
                        conn.update(sql, (var_list))

                # create new membership data
                if i == 2 and create:

                    # update var list
                    var_list.pop()
                    
                    # check if customer account exists
                    # if not create
                    if var_list[0] == "Nothing":
                        cus_id = uf.validate_customer_account(self.curr_user, True)                
                        var_list[0] = cus_id

                    # add next mem_id
                    var_list.insert(0, next_mem_id)

                    # create mem account
                    conn.insert(sql, (var_list))


                # delete membership details
                if i == 3 and delete:

                    if member_id == "None":
                        messagebox.showerror("Show Error","No membership to deactivate.")
                        raise ValueError("No membership to deactivate")
                    
                    else:   
                        conn.delete(sql, (member_id,))


            # commit & close
            conn.close(True)

            # update backing data
            self.get_user_info(False)

            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

    def user_password_updater(self) -> tuple[bool, str | None]:
        """
        check user inputs for username & curr/new passwords
        If successful, update db entree
        """

        try:
            conn = None
            output_msg = []

            data_list = [   
                ["username", str(self.username)],
                ["Curr_Password", str(self.curr_pass_var_entry.get().strip())],
                ["Password_1", str(self.new_pass_1_entry.get().strip())],
                ["Password_2", str(self.new_pass_2_entry.get().strip())]
            ]

            # check user inputs
            result = self.check_user_inputs_password(data_list)
            
            # if no error found, pass
            if result:
                messagebox.showerror("Validation Error", "\n".join(result))
                raise ValueError("Missing data within inputs")

            update_user_params = [
                str(self.curr_user),
                str(self.username),
                self.encryption(str(self.new_pass_1_entry.get().strip()),True),
                str(self.curr_user )            
            ]

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("user_data_create.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # update user password
                if i == 4:
                    conn.update(sql, update_user_params)

                    messagebox.showinfo("Show Info",f"Password Updated")
        
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

    def check_user_inputs_password(self, data_list) -> list:
        """
        check user inputs. List passed with username, curr_pass, new_pass 1 & 2
        Return output list of errors OR blank list
        """

        output_msg = []

        # check if data input str
        for i, data in enumerate(data_list):                
            if len(data[1]) == 0:
                output_msg.append(f'{data[0]}: Is missing input values')

        # check if password meets rules
        for i in data_list[2:3]:

            # char param to cross check
            special_characters = "!@#$%^&*()-+?_=,<>/"

            # length check
            if len(i[1]) < 12:
                output_msg.append(f"{i[0]} : Password must be at least 12 characters")

            # captilisation check
            if not any(c.isupper() for c in i[1]):
                output_msg.append(f"{i[0]} : Password must contain a capital letter")

            # check if number is present
            if not any(c.isdigit() for c in i[1]):
                output_msg.append(f"{i[0]} : Password must contain a number")

            # check if special char is present
            if not any(c in special_characters for c in i[1]):
                output_msg.append(f"{i[0]} : Password must contain a special character")

        # check if pass 1 / 2 match
        if str(data_list[2][1]) != str(data_list[3][1]):
            output_msg.append("New passwords must match")

        return output_msg

    def get_veh_info(self, update:bool, create: bool) -> tuple[bool, str | None]:
        """
        get_veh_info from curr_user passed into class

        :param self: self, pulled on setup & update details, update trigger from button pressed by user to update details
        :return: True is successful, or false and errorstring
        :rtype: tuple[bool, str | None]
        """

        try:
            conn = None
            params = ()
            sql_params = ()

            # get customer account, if not one. Create and return
            cus_acc = uf.validate_customer_account(self.curr_user, True)

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
                    
                if i == 6 and create:
                    
                    # get user inputs
                    params = (
                        self.car_reg_entry.get(),
                        self.car_make_entry.get(),
                        self.car_model_entry.get(),
                        self.mot_status_entry.get()
                    )

                    output_msg = []

                    # check if data input str               
                    for i, data in enumerate(params):

                        # check if none value
                        if data is None or data == "":
                            output_msg.append(f'Missing input values')

                    # check if date format dd/MM/yyyy >= today
                    if not self.is_valid_uk_reg(params[0]):
                        print("Invalid UK registration format (AA00 AAA)")

                    # check if date format dd/MM/yyyy >= today
                    # if true, correct input capitalisation
                    if params[3].lower() not in ['pass','fail']:
                        output_msg.append(f'MOT Status has to be "Pass", or "Fail"')
                    else:
                        if params[3].lower() == 'pass':
                            mot_status = "Pass"
                        else:
                            mot_status = "N/A"

                    # Return errors to user
                    if output_msg:
                        raise ValueError(output_msg)
                    
                    sql_params = (
                        next_veh_id,
                        self.customer_ref,
                        self.car_reg_entry.get(),
                        self.car_make_entry.get(),
                        self.car_model_entry.get(),
                        mot_status,
                        True
                    )

                    # create new veh
                    conn.insert(sql, sql_params)

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
                                active_flag,
                                username,
                                membership_id,
                                customer_id,
                                subscrip_pay_day,
                                payment_method,
                                iban
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

                            # set user param for utilisation in other frames
                            self.username = username
                            
                            # add all user membership data
                            self.membership_id = membership_id
                            self.customer_id = customer_id
                            self.subscrip_dat = subscrip_pay_day

                            if subscrip_pay_day is None:
                                subscrip_pay_day = '-'

                            self.payment_method = "Card"
                            self.iban = iban

                            if iban is None:
                                iban = '-'

                            self.membership_id_var.set("-")
                            self.customer_id_var.set("-")
                            self.subscrip_dat_entry.delete(0, tk.END)
                            self.payment_method_var.set("-")
                            self.iban_entry.delete(0, tk.END)

                            self.membership_id_var.set(membership_id)
                            self.customer_id_var.set(customer_id)
                            self.subscrip_dat_entry.insert(0, subscrip_pay_day)
                            self.payment_method_var.set(payment_method)   
                            self.iban_entry.insert(0, iban)
                            
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

                        messagebox.showinfo("Show Info","Account Details updated")
                        conn.commit()
                        self.get_user_info(False)

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

    def get_key(self):
        """ 
        get encryption key & store within obj
        """
        key_str = uf.get_encrypt_key()

        self.key = key_str.encode()
        self.f_key = Fernet(self.key)

    def encryption(self, input_data: str, encypt: bool) -> str:

        """
        input string to be encypted/decrypted
        encypt = True for  encypt, False = Decrypt
        key from store
        """
        if not self.f_key:
            raise ValueError("Fernet key not initialized")
        
        if encypt:
            return self.f_key.encrypt(input_data.encode()).decode()
        else:
            return self.f_key.decrypt(input_data.encode()).decode()

    def pw_requirements_printout(self):        
        """
        Docstring for pw_requirements_printout
        
        :param self
        """
        print_text = uf.password_requirements()

        messagebox.showinfo(
            print_text[0], 
            print_text[1]
            )

    def get_garagelist_details(self):
        """
        Docstring for get_garagelist_details
        
        :param self
        """
        print_text = uf.get_garagelist_details()

        messagebox.showinfo(
            print_text[0], 
            print_text[1]
            )

    def is_valid_uk_reg(self, reg: str) -> bool:
        """
        Docstring for is_valid_uk_reg
        
        :param self: Description
        :param reg: input str from customer veh
        :type reg: str
        :return: Return bool, if matching AA00 AAA (regex used)
        :rtype: bool
        """
        return bool(re.fullmatch(r'[A-Z]{2}\d{2} [A-Z]{3}', reg.upper()))