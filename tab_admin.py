import tkinter as tk
import utility_functions as uf
import xml_functions as xfc
from cryptography.fernet import Fernet
from tkinter import filedialog
from tkinter import messagebox
from tkinter import messagebox
from tkinter import ttk

class Tab7(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Administration Functions"
        self.controller = controller

        self.account_list = '-'
        self.access_code_list = '-'
        self.username = '-'

        self.db_table_list = '-'
        self.var_values = {}        
        self.var_widgets = {}
        self.load_file = '-'
        
        #encryption
        self.f_key = None
        self.get_key()

        ttk.Label(self, text="This is the Admin Funct Tab" \
        "\n> To change a users password or access code. Please select the account from the dropdown. Then input the new password/accesscode/activeflag. Active Flag has to be Active/Inactive, accesscode from respective lookup & password hit the rules."
        ).pack(pady=20)

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)

        # get data for frame contructions
        self.get_db_data()

        # frame  - Password Reseter
        # row 0, col 0
        self.password_reseter_frame = self.frame_1()

        # frame  - Database XML Backup Creator
        # row 1, col 0
        self.xml_database_backup = self.frame_2()

        # frame  - XML Importer
        # row 1, col 1
        self.xml_importer = self.frame_3()

        # get data for created frames
        self.user_updater_data(False)

    def frame_1(self):
        """
        constructor for frame 1 : password_reseter_frame
        """

        password_reseter_frame = tk.LabelFrame(self.frame, text="Password Reset")
        password_reseter_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
 
        # Labels
        tk.Label(password_reseter_frame, text="Select account to reset username and/or password. Once selected and data udpated press the 'Update Details' button.").grid(row=0, column=0)
        tk.Label(password_reseter_frame, text="Dropdown List for Accounts :").grid(row=1, column=0)

        self.username_var = tk.StringVar(value=self.username)
        tk.Label(password_reseter_frame, text="username").grid(row=2, column=0)
        tk.Label(password_reseter_frame, textvariable=self.username_var).grid(row=2, column=1)

        self.new_pass_var = tk.StringVar()
        tk.Label(password_reseter_frame, text="New Password").grid(row=3, column=0)
        self.new_pass_entry = tk.Entry(password_reseter_frame, textvariable=self.new_pass_var, show='*', width=40)
        self.new_pass_entry.grid(row=3, column=1, columnspan=2, sticky="we")

        self.access_code_var = tk.StringVar()
        tk.Label(password_reseter_frame, text="Access Code").grid(row=4, column=0)
        self.access_code_entry = tk.Entry(password_reseter_frame, textvariable=self.access_code_var, width=40)
        self.access_code_entry.grid(row=4, column=1, columnspan=2, sticky="we")

        self.active_flag_var = tk.StringVar()
        tk.Label(password_reseter_frame, text="Active Flag").grid(row=5, column=0)
        self.active_flag_entry = tk.Entry(password_reseter_frame, textvariable=self.active_flag_var, width=40)
        self.active_flag_entry.grid(row=5, column=1, columnspan=2, sticky="we")

        # entrys / combobox
        self.account_combobox = ttk.Combobox(password_reseter_frame, values=self.account_list)
        self.account_combobox.grid(row=1, column=1, columnspan=2, sticky="ew")

        udpate_usr_account = tk.Button(password_reseter_frame,text='Get Account Details',command=lambda: self.user_updater_data(False))
        udpate_usr_account.grid(row=1, column=3)

        update_usr_account = ttk.Button(password_reseter_frame,text='Update Details',command=lambda: self.user_updater_data(True))
        update_usr_account.grid(row=8, column=3)

        pw_requirement_details = tk.Button(password_reseter_frame,text='Password Requirements',command=self.pw_requirements_printout)
        pw_requirement_details.grid(row=3, column=3)

        accesscode_details = tk.Button(password_reseter_frame,text='Accesscode List',command=self.accesscode_printout)
        accesscode_details.grid(row=4, column=3)

        # format frame widgets
        for widget in password_reseter_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return password_reseter_frame

    def frame_2(self):
        """
        Constructor for frame 2: xml_database_backup with scrollable checkboxes
        """
        xml_database_backup = tk.LabelFrame(self.frame, text="Database XML backup Creator")
        xml_database_backup.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        # Label instructions
        tk.Label(
            xml_database_backup, 
            text="Uncheck any tables not required to be backed up. \nAll checked tables once the button is pressed will be created within ./data/ subfolder."
        ).grid(row=0, column=0, sticky="w")

        # Create a canvas and scrollbar
        canvas = tk.Canvas(xml_database_backup, width=200, height=200)
        scrollbar = tk.Scrollbar(xml_database_backup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Place canvas and scrollbar
        canvas.grid(row=1, column=0, sticky="nw")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Create a frame inside the canvas to hold checkboxes
        checkbox_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

        # Add checkboxes
        for i, value in enumerate(self.db_table_list):
            key = f"checkbox_var_{value}"
            self.var_values[key] = tk.IntVar(value=1)  # checkboxes created checked
            cb = tk.Checkbutton(checkbox_frame, text=value, variable=self.var_values[key])
            cb.grid(row=i, column=0, sticky="w")
            self.var_widgets[key] = cb

        # Update scrollregion whenever the frame changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        checkbox_frame.bind("<Configure>", on_frame_configure)

        # buttons
        create_db_backup = ttk.Button(xml_database_backup, text='Create backup', command=self.create_db_backup)
        create_db_backup.grid(row=2, column=0, pady=10, sticky="w")

        return xml_database_backup

    def frame_3(self):
        """
        Constructor for frame 3: xml_importer
        """
        xml_importer = tk.LabelFrame(self.frame, text="Database XML Importer")
        xml_importer.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        # Labels
        self.load_file_var = tk.StringVar(value=self.load_file)
        tk.Label(xml_importer, text="Previously Loaded File").grid(row=0, column=0)
        tk.Label(xml_importer, textvariable=self.load_file_var).grid(row=0, column=1)

        # buttons
        upload_xml_button = tk.Button(xml_importer, text="Upload xml file", command=self.select_file)
        upload_xml_button.grid(row=6, column=1)

        xml_requirements_printout = tk.Button(xml_importer, text="Get XML requirement Details", command=self.xml_requirements_printout)
        xml_requirements_printout.grid(row=7, column=1)

        # format frame widgets
        for widget in xml_importer.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return xml_importer

    def user_updater_data(self, update: bool) -> tuple[bool, str | None]:
        """
        update username/password or access code for selected user
        input update: this is to enact the update of a record, False updates only the backing data
        return True for success, or False & errorstring for failure (where applic)
        """

        try:
            # env params
            conn = None
            output_msg = []
            pw_update = False

            # get the account details from search/selector
            dropdown_checker = self.account_combobox.get()

            # if account has been selected. Generate backing data
            if dropdown_checker != '':
                self.edit_user_id = dropdown_checker[0:7]  

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("user_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # update user password
                if i == 4:
                    all_account_data = conn.query(sql, ())

                    if all_account_data:
                        output_list = []

                        # clean data into list
                        for i in all_account_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.account_list = output_list

                    # reset the combobox list on datarefresh
                    self.account_combobox['values'] = self.account_list
                    self.account_combobox.set('')

                # get account info from searcher dropdown                
                if i == 5 and dropdown_checker != '':

                    # clean entrees
                    self.username_var.set('')
                    self.new_pass_entry.delete(0, tk.END)
                    self.account_combobox.set('')
                    self.access_code_entry.delete(0, tk.END)
                    self.active_flag_entry.delete(0, tk.END)

                    # query db
                    account_info = conn.query(sql, (self.edit_user_id,))

                    # if data found for account selector, update self data
                    if account_info[1]:
                        rows = account_info[1]

                        if rows:
                            (
                                user_id,
                                access_code,
                                active_flag,
                                username
                            ) = rows[0]

                        # update edit/creation frame if true
                        # default = false, and Package Info frame updated
                        self.username_var.set(username)
                        self.new_pass_entry.insert(0,'')
                        self.access_code_entry.insert(0,access_code)

                        if active_flag == 1:
                            self.active_flag_entry.insert(0,"Active")
                            self.curr_active_flag = "Active"
                        if active_flag == 0:
                            self.active_flag_entry.insert(0,"Inactive")
                            self.curr_active_flag = "Inactive"

                        self.curr_access_code = access_code

                # get accesscode info               
                if i == 6:
                    all_accesscode_data = conn.query(sql, ())

                    if all_accesscode_data:
                        output_list = []

                        # clean data into list
                        for i in all_accesscode_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.access_code_list = output_list
     
                # update user account               
                if i == 7 and update:

                    # get input data
                    edit_user_id = self.edit_user_id
                    new_password = self.new_pass_entry.get().strip()
                    accesscode = self.access_code_entry.get()
                    activeflag = self.active_flag_entry.get()

                    # check if new password has been input
                    if new_password:
                        pw_update = True
                    
                    var_list = [
                        str(new_password),
                        str(accesscode),
                        str(activeflag)
                    ]

                    # check if inputs are ok
                    result = self.check_user_inputs_password(var_list)

                    # if no error found, pass
                    if result:
                        messagebox.showerror("Validation Error", "\n".join(result))
                        raise ValueError("Incorrect data inputs")

                    # check if accesscode/activeflag change
                    # if so, update user record
                    if self.curr_access_code != accesscode or self.curr_active_flag != activeflag:
                        
                        # conver active flag back to bool
                        if activeflag == "Active":
                            activeflag = 1
                        if activeflag == "Inactive":
                            activeflag = 0
                            
                        # update edit_user records details        
                        conn.update(sql, (accesscode, activeflag, edit_user_id))

                        output_msg.append("User account details updated")

                    # check if any change req.
                    # if not, alert user
                    if self.curr_access_code == accesscode and self.curr_active_flag == activeflag and pw_update == False:
                        messagebox.showinfo("Account Update", f"There is no change required on this account. Please ensure there is an update to a password/accesscode or activeflag.")

                # update password into login_details table         
                if i == 8 and pw_update:
                    
                    # encrypt pw to pass into db
                    encrypt_pw = self.encryption(str(new_password),True)

                    # update edit_user record details        
                    conn.update(sql, (encrypt_pw, edit_user_id))

                    # clean entrees
                    self.username_var.set('')
                    self.new_pass_entry.delete(0, tk.END)
                    self.account_combobox.set('')
                    self.access_code_entry.delete(0, tk.END)
                    self.active_flag_entry.delete(0, tk.END)

                    output_msg.append("Password for account updated")
            
            # if no errors found, pass
            if output_msg:
                messagebox.showinfo("Account Update", "\n".join(output_msg))

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

    def get_db_data(self) -> tuple[bool, list | None]:
        """
        Docstring for get_db_data
        
        :param self: pulled data
        :return: True for success, False & errorstring for failure
        :rtype: tuple[bool, str | None]
        """
        try:        

            # env params
            conn = None
            
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("admin_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # update user password
                if i == 0:
                    output_data = []
                    data = conn.query(sql, ())
                    
                    # clean data into list
                    for i in data[1]:
                        output_data.append(i[0])
                    
                    # add to self var
                    self.db_table_list = output_data
            
            # commit & close
            conn.close(True)

            return True, output_data

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

    def check_user_inputs_password(self, data_list) -> list:
        """
        check user inputs. Password, accesscode & activeflag
        Return output list of errors OR blank list
        """

        output_msg = []

        # skip if not pw update req.
        if data_list[0]:
            # check if data input str
            for i, data in enumerate(data_list):                
                if len(data[1]) == 0:
                    output_msg.append(f'{data[0]}: Is missing input values')

            # check if password meets rules        
            # char param to cross check
            special_characters = "!@#$%^&*()-+?_=,<>/"

            # length check
            if len(data_list[0]) < 12:
                output_msg.append(f"Password must be at least 12 characters")

            # captilisation check
            if not any(c.isupper() for c in data_list[0]):
                output_msg.append(f"Password must contain a capital letter")

            # check if number is present
            if not any(c.isdigit() for c in data_list[0]):
                output_msg.append(f"Password must contain a number")

            # check if special char is present
            if not any(c in special_characters for c in data_list[0]):
                output_msg.append(f"Password must contain a special character")

        # check input access code
        exist = any(data_list[1] in i for i in self.access_code_list)
        
        if not exist:
            output_msg.append(f"Access code input is not supported.")
 
        # check activeflag input = Active/Inactive
        if data_list[2] not in ["Active","Inactive"]:
            output_msg.append(f"Activeflag needs to be Active or Inactive")

        return output_msg

    def create_db_backup(self) -> tuple[bool, str | None]:
        """
        Docstring for create_db_backup
        
        :param self: Description
        :return: True for success, False & errorstring for failure
        :rtype: bool
        """
        try:
                
            db_list_backup = []

            # get status from created checkboxes
            for key, var in self.var_values.items():
                status = var.get()
                
                # if status is true (checked), creation = True
                if status:
                    temp_str = key
                    outstr = temp_str.replace("checkbox_var_","")
                    db_list_backup.append(outstr)

            # pass db_table list to create backups
            xfc.database_backup(db_list_backup)
            messagebox.showinfo("Backup Info","Backup created successfull into ./data/... folder")

            return True

        except Exception as err:
            messagebox.showerror("Error Info","Backup process error")
            print(f"Unexpected error: {err}, type={type(err)}")
            return False, str(err)

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

    def accesscode_printout(self):
        """
        Docstring for accesscode_printout
        
        :param self
        """
        print_text = uf.access_code_list()

        messagebox.showinfo(
            print_text[0], 
            print_text[1]
            )

    def xml_requirements_printout(self):
        """
        Docstring for xml_requirements_printout
        
        :param self
        """
        print_text = uf.xml_requirements()

        messagebox.showinfo(
            print_text[0], 
            print_text[1]
            )

    def select_file(self) -> tuple[bool, str | None]:
        """"
        file selector
        """
        
        try:

            # get filepath from user
            filepath = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("xml files", "*.xml")]
            )
            
            # check user filepath values
            if filepath == '' or filepath is None:
                messagebox.showerror("show info","File not selected")
                raise ValueError("No value file selected")                

            self.load_file = filepath
            self.load_file_var.set(self.load_file)

            # attempt to load file
            result = xfc.database_updater_from_xml(filepath)

            # check results of attempting to load file
            if result[0]:
                messagebox.showinfo("show info","File loaded successfully")

            else:
                messagebox.showerror("show error",f"Error when loading file please check the filenmae and all requirements")
                raise ValueError("Error on fileload")    

            return True

        except Exception as err: # Exception Block. Return data to user & False
            print(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
            return False, str(err)