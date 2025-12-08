import tkinter as tk
import icecream as ic
import utility_functions as uf
import image_functions as ifc
import registration_window as rg
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
from tkinter import PhotoImage, messagebox
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Tab7(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Administration Functions"
        self.controller = controller

        self.account_list = '-'
        self.username = '-'

        #encryption
        self.f_key = None
        self.get_key()

        ttk.Label(self, text="This is the Account Management Tab" \
        "\n> To change account details, including password. Please update the required fields and press the 'Update my details' button." \
        "\n> To update password, please input current password and then your new password (in both the first and second box), then 'Update my password', button." \
        "\n> To deactivate your account completely. Please tick the deactivation box, and input username and password. This will complete the process and close the application & deactivate your account. To reactivate, please untick the box when updating" \
        
        "\n\n> To add a new vehicle to your account, please within the 'Vehicle Information' window, add the details to the 4 boxes and press the 'Update/Add vehicle' button." \
        "\n> To update a vehicle, please select one vehicle from the dropdown box, update respective fields, and press'Update/Add vehicle' button. To deactivate a vehicle, check box to deactivate and press 'update my vehicle list', to reactivate, when updating untick the box." \
        "\n\n>To create a membership, input Card/Iban/day for payment then press 'Create/Update Details'. Update data displayed and press the 'Create/Update Details', to deactivate press the 'Deactivate my membership'" \
        "\n> To edit update data displayed and press the 'Create/Update Details', to deactivate press the 'Deactivate my membership'"
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

        # frame  - Password Reseter
        # row 0, col 0
        self.password_reseter_frame = self.frame_1()

        # get data for frames
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

        self.username_var = tk.StringVar()
        tk.Label(password_reseter_frame, text="Username").grid(row=2, column=0)
        self.username_entry = tk.Entry(password_reseter_frame, textvariable=self.username_var, width=40)
        self.username_entry.grid(row=2, column=1, columnspan=2, sticky="we")

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

        udpate_usr_account = tk.Button(password_reseter_frame,text='Update Details',command=lambda: self.user_updater_data(True))
        udpate_usr_account.grid(row=4, column=3)

        # format frame widgets
        for widget in password_reseter_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return password_reseter_frame

    def user_updater_data(self, update: bool) -> tuple[bool, str | None]:
        """
        update username/password or access code for selected user
        input update: this is to enact the update of a record, False updates only the backing data
        return True for success, or False & errorstring for failure (where applic)
        """

        try:
            conn = None

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

                # get package info from searcher dropdown                
                if i == 5 and dropdown_checker != '':

                    # clean entrees
                    self.username_entry.delete(0, tk.END)
                    self.new_pass_entry.delete(0, tk.END)
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
                        self.username_entry.insert(0,username)
                        self.new_pass_entry.insert(0,'')
                        self.access_code_entry.insert(0,access_code)

                        if active_flag == 1:
                            self.active_flag_entry.insert(0,"Active")
                        if active_flag == 0:
                            self.active_flag_entry.insert(0,"Inactive")

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
        for i in data_list[1]:

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