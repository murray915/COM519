import tkinter as tk
import icecream as ic
import utility_functions as uf


class Login_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Login Window')

        #ttk.Button(self,text='Close',command=self.destroy).pack(expand=True)

        usernameLabel = tk.Label(self, text="User Name").grid(row=0, column=0)
        self.username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=self.username).grid(row=0, column=1)

        # Password label and password entry box
        passwordLabel = tk.Label(self, text="Password").grid(row=1, column=0)
        self.password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=self.password, show='*').grid(row=1, column=1)

        # Login button
        loginButton1 = tk.Button(self, text="Login", command=self.validateLogin).grid(row=3, column=0)

       # register
       # loginButton2 = tk.Button(self, text="Register", command=self.register_customer).grid(row=3, column=1)


    def validateLogin(self):
        # Login check
        value_username = self.username.get()
        value_password = str(self.password.get())

        db = uf.get_database_connection()

        if not db:
            ic("Database connection error")
            return 

        login_query = uf.load_sql_file("logincheck.sql")
        result = db.query(login_query, (value_username, value_password))

        ic(result, value_username, value_password)
