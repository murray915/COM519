import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from icecream import ic
import utility_functions as uf
from cryptography.fernet import Fernet


class Reg_Window(tk.Toplevel):
    def __init__(self, parent=None, test_mode=False):
        if test_mode:
            # testmode stops all Tk operations
            # i.e. window creations
            self.first_name = tk.StringVar()
            self.surname_name = tk.StringVar()
            self.add_1 = tk.StringVar()
            self.add_2 = tk.StringVar()
            self.add_3 = tk.StringVar()
            self.post_code = tk.StringVar()
            self.email_add = tk.StringVar()
            self.phone_no = tk.StringVar()
            self.username = tk.StringVar()
            self.password = tk.StringVar()  
            return
                       
        if parent is None:
            parent = tk.Tk()

        super().__init__(parent)

        #encryption
        self.f_key = None
        self.get_key()

        # window params
        self.geometry(uf.get_settings_data()["ktinker_settings"]["reg_geometry"])
        self.title('Registration Window')
        
        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame setup - 1
        user_info_frame = tk.LabelFrame(self.frame, text="User Information")
        user_info_frame.grid(row=0, column=0, padx=20, pady=20)

        # frame get data
        # labels
        tk.Label(user_info_frame, text="First Name").grid(row=0, column=0)
        tk.Label(user_info_frame, text="Surname").grid(row=0, column=1)
        tk.Label(user_info_frame, text="Address 1").grid(row=2, column=0)
        tk.Label(user_info_frame, text="Address 2").grid(row=2, column=1)
        tk.Label(user_info_frame, text="Address 3").grid(row=2, column=2)
        tk.Label(user_info_frame, text="Postcode").grid(row=2, column=3)
        tk.Label(user_info_frame, text="Email Address").grid(row=4, column=1)
        tk.Label(user_info_frame, text="Phone Number").grid(row=4, column=2)

        # variables
        self.first_name = tk.StringVar()
        self.surname_name = tk.StringVar()
        self.add_1 = tk.StringVar()
        self.add_2 = tk.StringVar()
        self.add_3 = tk.StringVar()
        self.post_code = tk.StringVar()
        self.email_add = tk.StringVar()
        self.phone_no = tk.StringVar()

        # entrys
        self.first_name_entry = tk.Entry(user_info_frame, textvariable=self.first_name)
        self.first_name_entry.grid(row=1, column=0)
        self.surname_name_entry = tk.Entry(user_info_frame, textvariable=self.surname_name)
        self.surname_name_entry.grid(row=1, column=1)
        self.add_1_entry = tk.Entry(user_info_frame, textvariable=self.add_1)
        self.add_1_entry.grid(row=3, column=0)
        self.add_2_entry = tk.Entry(user_info_frame, textvariable=self.add_2)
        self.add_2_entry.grid(row=3, column=1)
        self.add_3_entry = tk.Entry(user_info_frame, textvariable=self.add_3)
        self.add_3_entry.grid(row=3, column=2)
        self.post_code_entry = tk.Entry(user_info_frame, textvariable=self.post_code)
        self.post_code_entry.grid(row=3, column=3)
        self.email_add_entry = tk.Entry(user_info_frame, textvariable=self.email_add)
        self.email_add_entry.grid(row=5, column=1)
        self.phone_no_entry = tk.Entry(user_info_frame, textvariable=self.phone_no)
        self.phone_no_entry .grid(row=5, column=2)

        # format frame widgets
        for widget in user_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # frame setup - 2
        login_details_frame = tk.LabelFrame(self.frame)
        login_details_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)

        # frame get data
        # labels
        tk.Label(login_details_frame, text="Username").grid(row=0, column=1)
        tk.Label(login_details_frame, text="Password").grid(row=0, column=2)

        # varibles
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # entrys
        self.username_entry = tk.Entry(login_details_frame, textvariable=self.username)
        self.username_entry.grid(row=1, column=1)
        self.password_entry = tk.Entry(login_details_frame, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=2)

        # format frame widgets
        for widget in login_details_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # frame setup - 3
        ts_cs_frame = tk.LabelFrame(self.frame)
        ts_cs_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)

        # frame get data
        # labels
        tcs_label = tk.Label(ts_cs_frame, text="Terms & Conditions")
        tcs_label.grid(row=0, column=1)
        tcs_check = tk.Checkbutton(tcs_label, text="Accept Terms & Conditions")
        tcs_check.grid(row=0, column=2)

        ttk.Button(self,text='Create User Account',command=self.validate_user_inputs).pack(expand=True)
        ttk.Button(self,text='Terms & Conditions',command=self.tcs_printout).pack(expand=True)
        ttk.Button(self,text='Close',command=self.destroy).pack(expand=True)


    def tcs_printout(self):
        messagebox.showinfo(
            "Terms & Conditions", 
            "By accepting the terms and conditions of this application, you have agreed to:" \
                "\n1. Look over any spelling mistakes" \
                "\n2. Agree that actually green is the best colour" \
                "\n3. That this application & report deserve a 1st" \
                "\n >> Thank you for agreeing to the terms & conditions <<" \
                "\n  Recording of the acceptance will be in the audit tables "
                )
        

    def validate_user_inputs(self, create=True) -> bool:
        """
        check user information > if return True
        check username/password > if return True
        Register user
        Else, return error to user as msgbox . Per function
        """

        # Step 1: User info
        reg_ok = self.validate_user_information_data()

        if not reg_ok:
            return False

        # Step 2: Login data
        reg_ok = self.validate_user_login_data()

        if not reg_ok:
            return False

        # Step 2: Login data
        postcode_id = self.validate_postcode(None,create)
        
        # final step: create user/login_details
        result = self.register_customer(postcode_id, create)

        ic(result)

        if result == False:
            return False      
                       
        # If both valid, true
        return True


    def validate_user_information_data(self) -> bool | str:
        """
        check user input data, create message box with all required actions
        """

        try:
            output_msg = []

            str_check_list = [
                ["First Name", self.first_name.get().strip()]
                ,["Surname", self.surname_name.get().strip()]
                ,["Address 1", self.add_1.get().strip()]
                ,["Address 2", self.add_2.get().strip()]
                ,["Email Address", self.email_add.get().strip()]
                ,["Postcode", self.post_code.get().strip().strip(" ")]
                ]  
                      
            int_check_list = [
                 ["Phone Number", self.phone_no.get().strip()]
                 ]
            
            # check if data input str
            for label, data in str_check_list:                
                if len(data) == 0:
                    output_msg.append(f'{label}: Is missing input values')

            # check if data input int
            for label, value in int_check_list:
                if len(value) == 0:
                    output_msg.append(f"{label}: Is missing input values")
                    
                if not value.isdigit():
                    output_msg.append(f"{label}: Is incorrect, \"{value}\" not a number")

            for i in output_msg:
                ic(i)

            if output_msg:
                messagebox.showerror("Validation Error", "\n".join(output_msg))
                return False

            # if nothing added to output_msg all validated
            if len(output_msg) == 0:
                ic('successful validation step 1')
                return True                

            return False
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return err


    def validate_user_login_data(self) -> bool:
        """
        check user login data, create message box with all required actions
        -Username has to be unique
        -password has to meet conditions:
            12 len
            1 capitalized letter
            1 special char
            1 number
        """

        try:
            output_msg = []

            data_list = [   
                ["username", str(self.username.get().strip())],
                ["Password", str(self.password.get().strip())]
                ]

            # check if data input str
            for i, data in enumerate(data_list):                
                if len(data[1]) == 0:
                    output_msg.append(f'{data[0]}: Is missing input values')

            # check if username is avalible
            if len(output_msg) == 0:
                input_username = str(self.username.get().strip())

                # db connection
                conn = uf.get_database_connection()

                sql = uf.load_sql_file("user_data_get.sql")
                result = conn.query(sql, (input_username,))

                conn.close()

                if result[1]:
                    output_msg.append(f'{input_username}: Has already been used. Please try another username')
                                
            # check if password meets rules
            if len(output_msg) == 0:
                input_username = self.password.get().strip()
                special_characters = "!@#$%^&*()-+?_=,<>/"

                if len(input_username) < 12:
                    output_msg.append("Password must be at least 12 characters")

                if not any(c.isupper() for c in input_username):
                    output_msg.append("Password must contain a capital letter")

                if not any(c.isdigit() for c in input_username):
                    output_msg.append("Password must contain a number")

                if not any(c in special_characters for c in input_username):
                    output_msg.append("Password must contain a special character")

                if output_msg:
                    messagebox.showerror("Validation Error", "\n".join(output_msg))
                    return False

            if len(output_msg) == 0:
                ic('successful validation step 2')                
                return True
            
            return False
    
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return err


    def validate_postcode(self, input_postcode=None, create=True) -> str:
        """
        Check if postcode input exists in db
        If exist return id, if not create & return postcode_id
        create default True, if testing, pass False        
        """

        # get postcode data
        if input_postcode is None:
            postcode = self.post_code.get().strip().strip(" ")
        else:
            postcode = input_postcode

        # get result if exist or not
        result = uf.validate_postcode(postcode, create)

        return result


    def register_customer(self, postcode_id: str, create=True) -> bool | str:
        """
        Data validation completed. Create user skeletal record
        input postcode_id from function
        input create = False if testing and creation into db not req.
        """
        
        try:
                conn = None
                
                user_params = [
                    (self.first_name.get() + " " + self.surname_name.get()),
                    (self.add_1.get()+" "+self.add_2.get()+" "+self.add_3.get()),
                    postcode_id,
                    self.email_add.get(),
                    self.phone_no.get()
                ]

                login_params = [
                    str(self.username.get().strip()),
                    self.encryption(str(self.password.get()),True)               
                ]

                ic(user_params, login_params)

                # db connection & sql script get
                conn = uf.get_database_connection()
                sql = uf.load_sql_file("user_data_create.sql")
                sql_statements = sql.replace("\n", "").split(";")

                # enact sql scripts (3 total)
                for i, sql in enumerate(sql_statements):

                    # get next id
                    if i == 0:
                        user_id = conn.query(sql, ())
                        user_id = user_id[1][0][0]

                        # update params with id
                        user_params.insert(0, user_id)
                        login_params.insert(0, user_id)

                    # create user record
                    if i == 1:
                        conn.insert(sql, user_params)

                    # create login_details record
                    if i == 2:
                        conn.insert(sql, login_params)

                    # check created records
                    if i == 3:
                        result = conn.query(sql, (user_id,))

                # commit records (false=testing)
                # close db connection
                if create:
                    conn.commit()

                conn.close()

                # check results if created update user
                # close window
                if result[1]:
                    messagebox.showinfo("showinfo", "New Account Registered. Please login to the application")
                    self.destroy()
                    return True
                
                # Else, return err to user
                else:
                    messagebox.showinfo("showinfo", "Failure on Account Creation. Please refer to System Admin")
                    return False
                

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass
            return err
        

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