import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from icecream import ic
from cryptography.fernet import Fernet
import utility_functions as uf
import registration_window as rg


class Login_Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(uf.get_settings_data()["ktinker_settings"]["login_geometry"])
        self.title('Login Window')
        self.key = None # updated in func
        self.f_key = None  # updated in func
        self.get_key()
        self.result = None

        usernameLabel = tk.Label(self, text="User Name").grid(row=0, column=0)
        self.username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=self.username).grid(row=0, column=1)

        # Password label and password entry box
        passwordLabel = tk.Label(self, text="Password").grid(row=1, column=0)
        self.password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=self.password, show='*').grid(row=1, column=1)

        # Login button
        loginButton = tk.Button(self, text="Login", command=self.validateLogin).grid(row=3, column=1)

        # register       
        ttk.Button(self,text='Register', command=self.open_window).grid(row=5, column=1)

        # close APP
        ttk.Button(self,text='Close',command=self.destroy).grid(row=6, column=4)

    def get_key(self):
        """ 
        get encryption key & store within obj
        """
        key_str = uf.get_encrypt_key()

        self.key = key_str.encode()
        self.f_key = Fernet(self.key)


    def run(self) -> bool:
        """
        function to trigger ktinker & loop
        Returned login success/fail bool
        """
        self.mainloop()
        return self.result


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


    def validateLogin(self) -> bool | str:
        """
        On login button press. Check details within db to validate
        Encryption/Descryption completed in separate function
        returned true/false on login OR if error str error
        """
        
        try:
                
            # Login check
            value_username = self.username.get().strip()
            value_password = self.encryption(str(self.password.get()),True)

            # get database connection
            db = uf.get_database_connection()

            # if connection, validate login
            if db:

                login_query = uf.load_sql_file("login_check.sql")
                result = db.query(login_query, (value_username,))

                db.close() 

                # if username found check pass
                if result[1]:

                    # check if password input  matches
                    if self.encryption(result[1][0][-1],False) == str(self.password.get()):
                        self.result = True
                        messagebox.showinfo("showinfo", "correct login and password")
                        self.result = [result[1][0][0],result[1][0][6]]
                        self.destroy()
                    else: # failed, return error to user
                        self.result = False
                        messagebox.showwarning("Warning", "Incorrect password")      
                                
                else:
                    self.result = False
                    messagebox.showwarning("Warning", "Incorrect login or password")      
                                
            # connection failed
            else:
                ic("Database connection error")            
                return "Database connection error"
            
            # completed process
            return self.result
        
        except Exception as err:
            ic(f"Unexpected error: {err}, type={type(err)}")
            return err


    def open_window(self):
        window = rg.Reg_Window(self)
        #for visibility on top level
        window.grab_set()