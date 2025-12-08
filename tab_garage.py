import tkinter as tk
import utility_functions as uf
from tkinter import messagebox
from tkinter import ttk

class Tab6(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Garages"
        self.controller = controller

        self.garage_id = '-'
        self.garage_name = '-'
        self.address = '-'
        self.postcode_id = '-'
        self.postcode = '-'
        self.email = '-'
        self.phoneno = '-'
        self.contact_staff = '-'

        self.garge_list = '-'

        self.check_var = None

        ttk.Label(self, text="This is the Garage Management Tab" \
        "\n> To view garages please select the required garage from the left frame, and press the 'get garage data' button."
        "\n> To edit/create new garages, in the right frame, please select the garage to edit (if this is required), then 'get garage data'. " \
        "\n\tThe tickbox will check automatically, to EDIT please keep ticked, to create a new record untick this box."    
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

        # frame 1 - Garage Info
        # row 0, col 0
        self.garage_info_frame = self.frame_1()

        # frame 2 - Garage Edit/Add
        # row 0, col 1
        self.garage_edit_create_frame = self.frame_2()

        self.get_garage_info()

    def frame_1(self) -> object:
        """
        constructor for frame 1 : garage_info_frame
        """

        garage_info_frame = tk.LabelFrame(self.frame, text="Garage Information")
        garage_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
        # Labels
        tk.Label(
        garage_info_frame,
        text=(
            "Select the Garage to view from the dropdown"
            )
        ).grid(row=0, column=0)
        tk.Label(garage_info_frame, text="Dropdown List for Garages :").grid(row=1, column=0)

        self.garage_id_var = tk.StringVar(value=self.garage_id)
        tk.Label(garage_info_frame, text="Garage ID").grid(row=2, column=0)
        tk.Label(garage_info_frame, textvariable=self.garage_id_var).grid(row=2, column=1)

        self.garage_name_var = tk.StringVar(value=self.garage_name)
        tk.Label(garage_info_frame, text="Garage Name").grid(row=3, column=0)
        tk.Label(garage_info_frame, textvariable=self.garage_name_var).grid(row=3, column=1)

        self.address_var = tk.StringVar(value=self.address)
        tk.Label(garage_info_frame, text="Garage Address").grid(row=4, column=0)
        tk.Label(garage_info_frame, textvariable=self.address_var).grid(row=4, column=1)

        self.postcode_var = tk.StringVar(value=self.postcode)
        tk.Label(garage_info_frame, text="Postcode").grid(row=5, column=0)
        tk.Label(garage_info_frame, textvariable=self.postcode_var).grid(row=5, column=1)

        self.email_var = tk.StringVar(value=self.email)
        tk.Label(garage_info_frame, text="Email").grid(row=6, column=0)
        tk.Label(garage_info_frame, textvariable=self.email_var).grid(row=6, column=1)

        self.phoneno_var = tk.StringVar(value=self.phoneno)
        tk.Label(garage_info_frame, text="Phone Number").grid(row=7, column=0)
        tk.Label(garage_info_frame, textvariable=self.phoneno_var).grid(row=7, column=1)

        self.contact_staff_var = tk.StringVar(value=self.contact_staff)
        tk.Label(garage_info_frame, text="Contact Staff").grid(row=8, column=0)
        tk.Label(garage_info_frame, textvariable=self.contact_staff_var).grid(row=8, column=1)

        # entrys / combobox
        self.garge_list_combobox = ttk.Combobox(garage_info_frame, values=self.garge_list)
        self.garge_list_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

        update_item_data = tk.Button(garage_info_frame, text="Get Garage Data", command=self.get_garage_info)
        update_item_data.grid(row=0, column=4)

        # format frame widgets
        for widget in garage_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return garage_info_frame
    
    def frame_2(self) -> object:
        """
        constructor for frame 3 : garage_edit_create_frame
        """
        
        garage_edit_create_frame = tk.LabelFrame(self.frame, text="Garage Edit / Creation")
        garage_edit_create_frame.grid(row=0, column=3, columnspan=3, padx=10, pady=10)

        # Labels
        tk.Label(
                garage_edit_create_frame,
                text=(
                    "To edit an existing Garage please select the package from the dropdown.\n"
                    "The checkbox will denote that this is edit and not creation.\n"
                    "NOTE: If unticked, a new record within current inputs will be created"
                    )
                ).grid(row=0, column=0)
        tk.Label(garage_edit_create_frame, text="Dropdown List for Garages :").grid(row=1, column=0)

        self.garage_id_edit_var = tk.StringVar(value=self.garage_id)
        tk.Label(garage_edit_create_frame, text="Garage ID").grid(row=2, column=0)
        tk.Label(garage_edit_create_frame, textvariable=self.garage_id_edit_var).grid(row=2, column=1)

        self.garage_name_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Garage Name").grid(row=3, column=0)
        self.garage_name_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.garage_name_edit_var, width=40)
        self.garage_name_edit_entry.grid(row=3, column=1, columnspan=2, sticky="we")

        self.address_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Garage Address").grid(row=4, column=0)
        self.garage_address_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.address_edit_var, width=40)
        self.garage_address_edit_entry.grid(row=4, column=1, columnspan=2, sticky="we")

        self.postcode_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Postcode").grid(row=5, column=0)
        self.garage_postcode_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.postcode_edit_var, width=40)
        self.garage_postcode_edit_entry.grid(row=5, column=1, columnspan=2, sticky="we")

        self.email_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Email").grid(row=6, column=0)
        self.garage_email_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.email_edit_var, width=40)
        self.garage_email_edit_entry.grid(row=6, column=1, columnspan=2, sticky="we")

        self.phoneno_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Phone Number").grid(row=7, column=0)
        self.garage_phoneno_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.phoneno_edit_var, width=40)
        self.garage_phoneno_edit_entry.grid(row=7, column=1, columnspan=2, sticky="we")

        self.contact_staff_edit_var = tk.StringVar()
        tk.Label(garage_edit_create_frame, text="Phone Number").grid(row=7, column=0)
        self.garage_contact_staff_edit_entry = tk.Entry(garage_edit_create_frame, textvariable=self.contact_staff_edit_var, width=40)
        self.garage_contact_staff_edit_entry.grid(row=7, column=1, columnspan=2, sticky="we")

        # entrys / combobox
        self.garge_list_edit_combobox = ttk.Combobox(garage_edit_create_frame, values=self.garge_list)
        self.garge_list_edit_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

        self.check_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(garage_edit_create_frame, text="Edit Record", variable=self.check_var)
        self.checkbox.grid(row=1, column=4)

        get_package_data = tk.Button(garage_edit_create_frame, text="Get Garage Data", command=self.get_garage_edit_create)
        get_package_data.grid(row=0, column=4)

        update_package_data = tk.Button(garage_edit_create_frame, text="Update/Create Garage Data", command=lambda: self.get_garage_edit_create(True))
        update_package_data.grid(row=7, column=4)

        # format frame widgets
        for widget in garage_edit_create_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return garage_edit_create_frame

    def get_garage_info(self) -> tuple[bool, str | None]:
        """
        get garage information from dropdown combobox selector

        return bool for success and errorstring (whereapplic)
        """
        try:
            conn = None

            # get the part_id from search/selector
            dropdown_checker = self.garge_list_combobox.get()

            if dropdown_checker != '':
                self.garage_id = dropdown_checker[0:8]                           

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("garage_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next garage id
                if i == 0:
                    next_garage_id = conn.query(sql, ())
                    next_garage_id = next_garage_id[1][0][0]

                # get all garage_id data for dropdown
                if i == 1 and dropdown_checker == '':
                    all_garage_data = conn.query(sql, ())

                    if all_garage_data:
                        output_list = []

                        # clean data intp list
                        for i in all_garage_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.garge_list = output_list
            
                    # reset the combobox list on datarefresh
                    self.garge_list_combobox['values'] = self.garge_list
                    self.garge_list_combobox.set('')

                    self.garge_list_edit_combobox['values'] = self.garge_list
                    self.garge_list_edit_combobox.set('')

                # set garage detials
                if i == 4 and dropdown_checker != '':
                    
                    # get data
                    data = conn.query(sql, (self.garage_id,))

                    # if data found for search/item selector, update self data
                    if data[1]:
                        rows = data[1]

                        if rows:
                            (
                                garage_id,
                                name,
                                address,
                                postcode,
                                email,
                                phonenumber,
                                contact_staff
                            ) = rows[0]

                        # set data within table
                        self.garage_id_var.set(garage_id)
                        self.garage_name_var.set(name)
                        self.address_var.set(address)
                        self.postcode_var.set(postcode)
                        self.email_var.set(email)
                        self.phoneno_var.set(phonenumber)
                        self.contact_staff_var.set(contact_staff)

                    # clear searchbox
                    self.garge_list_combobox.set('')


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

    def get_garage_edit_create(self, action=False) -> tuple[bool, str | None]:
        """
        get garage information from dropdown combobox selector
        action = False by default. If True, then edit/create requested by user

        return bool for success and errorstring (whereapplic)
        """
        try:
            conn = None

            # get the part_id from search/selector
            dropdown_checker = self.garge_list_edit_combobox.get()

            if dropdown_checker != '':
                self.garage_id = dropdown_checker[0:8]                           

                # check the edit box
                self.check_var.set(True)

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("garage_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next package_id
                if i == 0:
                    self.next_garage_id = conn.query(sql, ())
                    self.next_garage_id = self.next_garage_id[1][0][0]
                
                # get package info from searcher dropdown                
                if i == 4 and dropdown_checker != '':

                    # cleanup previous inputs
                    self.garage_id_edit_var.set("-")
                    self.garage_name_edit_entry.delete(0, tk.END)
                    self.garage_address_edit_entry.delete(0, tk.END)
                    self.garage_postcode_edit_entry.delete(0, tk.END)
                    self.garage_email_edit_entry.delete(0, tk.END)
                    self.garage_phoneno_edit_entry.delete(0, tk.END)
                    self.garage_contact_staff_edit_entry.delete(0, tk.END)
                                
                    # get data
                    data = conn.query(sql, (self.garage_id,))

                    # if data found for search/item selector, update self data
                    if data[1]:
                        rows = data[1]

                        if rows:
                            (
                                garage_id,
                                name,
                                address,
                                postcode,
                                email,
                                phonenumber,
                                contact_staff
                            ) = rows[0]

                        # set data within table
                        self.garage_id_edit_var.set(garage_id)
                        self.garage_name_edit_entry.insert(0, name)
                        self.garage_address_edit_entry.insert(0, address)
                        self.garage_postcode_edit_entry.insert(0, postcode)
                        self.garage_email_edit_entry.insert(0, email)
                        self.garage_phoneno_edit_entry.insert(0, phonenumber)
                        self.garage_contact_staff_edit_entry.insert(0, contact_staff)

                    # clear searchbox
                    self.garge_list_edit_combobox.set('')

                # update existing record
                # action = True button pressed by user
                if i == 5 and action:

                    # get user input params
                    garage_id = self.garage_id
                    name = self.garage_name_edit_entry.get()
                    address = self.garage_address_edit_entry.get()
                    postcode = self.garage_postcode_edit_entry.get()
                    email = self.garage_email_edit_entry.get()
                    phonenumber = str(self.garage_phoneno_edit_entry.get())
                    contact_staff = self.garage_contact_staff_edit_entry.get()
                
                    variable_list = [
                        str(name),
                        str(address),
                        postcode,
                        str(email),
                        str(phonenumber),
                        str(contact_staff),
                        garage_id
                    ]

                    # check for user inputs into all boxes
                    if any(not var for var in variable_list):
                        messagebox.showerror("Show Error","Please ensure all boxes are populated")
                        raise ValueError("Missing data within inputs")

                    # get postcode_id
                    # creates if not within db table
                    postcode_id = uf.validate_postcode(postcode, True)
                    variable_list[2] = postcode_id

                    # check the edit box
                    state = self.check_var.get()

                    if state:                        
                        # edit enabled
                        conn.update(sql, (variable_list))
                        messagebox.showinfo("Show Info",f"Garage {name} has been updated")

                        # cleanup previous inputs
                        self.garage_id_edit_var.set("-")
                        self.garage_name_edit_entry.delete(0, tk.END)
                        self.garage_address_edit_entry.delete(0, tk.END)
                        self.garage_postcode_edit_entry.delete(0, tk.END)
                        self.garage_email_edit_entry.delete(0, tk.END)
                        self.garage_phoneno_edit_entry.delete(0, tk.END)
                        self.garage_contact_staff_edit_entry.delete(0, tk.END)

                # create new existing record
                # action = True button pressed by user
                if i == 6 and action:

                    # check the edit box is unticket (thus create new record)
                    state = self.check_var.get()
                    if not state:
                        # edit var list. Move garage_id from end to front
                        variable_list.insert(0, self.next_garage_id)
                        variable_list.pop()

                        # create new record 
                        conn.insert(sql, (variable_list))

                    messagebox.showinfo("Show Info",f"New item {self.next_garage_id} , {name} has been created")

                    # cleanup previous inputs
                    self.garage_id_edit_var.set("-")
                    self.garage_name_edit_entry.delete(0, tk.END)
                    self.garage_address_edit_entry.delete(0, tk.END)
                    self.garage_postcode_edit_entry.delete(0, tk.END)
                    self.garage_email_edit_entry.delete(0, tk.END)
                    self.garage_phoneno_edit_entry.delete(0, tk.END)
                    self.garage_contact_staff_edit_entry.delete(0, tk.END)

            # commit & close
            conn.close(True)            

            # get update to dropdowns
            self.get_garage_info()

            return True
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)