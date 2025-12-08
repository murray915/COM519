import tkinter as tk
import icecream as ic
import utility_functions as uf
import image_functions as ifc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Tab4(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Packages"
        self.controller = controller

        self.package_id = '-'
        self.package_name = '-'
        self.description = '-'
        self.items_consumed = '-'
        self.active_flag = '-'
        self.package_list = '-'

        self.check_var = None

        ttk.Label(self, text="This is the Package Management Tab" \
        "\n> To view packages please select the required package from the left frame, and press the 'get package data' button."
        "\n> To edit/create new packages, in the right frame, please select the package to edit (if this is required), then 'get package data'. " \
        "\n\tThe tickbox will check automatically, to EDIT please keep ticked, to create a new record untick this box."    
        "\n> Graph at the bottom of the window is the consumed packages over time"
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

        # frame 1 - Package Info
        # row 0, col 0
        self.item_info_frame = self.frame_1()

        # frame 2 - Package Purchased Overtime
        # row 1, col 0
        self.package_purch_graph_frame = self.frame_2()      

        # frame 3 - Package Edit/Create
        # row 0, col 1
        self.item_info_frame = self.frame_3()

        # get background data
        self.get_package_info()

    def frame_1(self) -> object:
        """
        constructor for frame 1 : package_info_frame
        """

        package_info_frame = tk.LabelFrame(self.frame, text="Package Information")
        package_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
        # Labels
        tk.Label(
        package_info_frame,
        text=(
            "Select the package to view from the dropdown"
            )
        ).grid(row=0, column=0)
        tk.Label(package_info_frame, text="Dropdown List for Packages :").grid(row=1, column=0)

        self.package_id_var = tk.StringVar(value=self.package_id)
        tk.Label(package_info_frame, text="Package ID").grid(row=2, column=0)
        tk.Label(package_info_frame, textvariable=self.package_id_var).grid(row=2, column=1)

        self.package_name_var = tk.StringVar(value=self.package_name)
        tk.Label(package_info_frame, text="Package Name").grid(row=3, column=0)
        tk.Label(package_info_frame, textvariable=self.package_name_var).grid(row=3, column=1)

        self.description_var = tk.StringVar(value=self.description)
        tk.Label(package_info_frame, text="Package Description").grid(row=4, column=0)
        tk.Label(package_info_frame, textvariable=self.description_var).grid(row=4, column=1)

        self.items_consumed_var = tk.StringVar(value=self.items_consumed)
        tk.Label(package_info_frame, text="Items Within Package").grid(row=5, column=0)
        tk.Label(package_info_frame, textvariable=self.items_consumed_var).grid(row=5, column=1)

        self.activeflag_var = tk.StringVar(value=self.active_flag)
        tk.Label(package_info_frame, text="Active Flag").grid(row=6, column=0)
        tk.Label(package_info_frame, textvariable=self.activeflag_var).grid(row=6, column=1)

        # entrys / combobox
        self.package_combobox = ttk.Combobox(package_info_frame, values=self.package_list)
        self.package_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

        update_item_data = tk.Button(package_info_frame, text="Get Package Data", command=self.get_package_info)
        update_item_data.grid(row=0, column=4)

        # format frame widgets
        for widget in package_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return package_info_frame

    def frame_2(self) -> object:
        """
        constructor for frame 2 : package_purch_graph_frame
        """

        try:
            conn = None

            package_purch_graph_frame = tk.LabelFrame(self.frame, text="Item Consumption Data")
            package_purch_graph_frame.grid(row=1, column=0, columnspan=10, padx=10, pady=10)
    
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("package_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get specific item_id data
                if i == 6:       
                    data = conn.query(sql, ())

            fig = uf.build_matplot_objects_stocktab(data, "Package Consumption per Package (by Month)","Year-Month","Package QTY Consumed","package_id","count_package_booked")

            # create canvas & plot graph
            canvas = FigureCanvasTkAgg(fig, master=package_purch_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            return True, None

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

    def frame_3(self) -> object:
        """
        constructor for frame 3 : package_edit_create_frame
        """
        
        package_edit_create_frame = tk.LabelFrame(self.frame, text="Package Edit / Creation")
        package_edit_create_frame.grid(row=0, column=5, columnspan=3, padx=10, pady=10)

        # Labels
        tk.Label(
                package_edit_create_frame,
                text=(
                    "To edit an existing please select the package from the dropdown.\n"
                    "The checkbox will denote that this is edit and not creation.\n"
                    "NOTE: If unticked, a new record within current inputs will be created"
                    )
                ).grid(row=0, column=0)
        tk.Label(package_edit_create_frame, text="Dropdown List for Packages :").grid(row=1, column=0)

        self.package_id_var_f3 = tk.StringVar(value=self.package_id)
        tk.Label(package_edit_create_frame, text="Package ID").grid(row=2, column=0)
        tk.Label(package_edit_create_frame, textvariable=self.package_id_var_f3).grid(row=2, column=1)

        self.package_name = tk.StringVar()
        tk.Label(package_edit_create_frame, text="Package Name").grid(row=3, column=0)
        self.package_name_entry = tk.Entry(package_edit_create_frame, textvariable=self.package_name)
        self.package_name_entry.grid(row=3, column=1)

        self.description = tk.StringVar()
        tk.Label(package_edit_create_frame, text="Package Description").grid(row=4, column=0)
        self.description_entry = tk.Entry(package_edit_create_frame, textvariable=self.description)
        self.description_entry.grid(row=4, column=1)

        self.items_consumed = tk.StringVar()
        tk.Label(package_edit_create_frame, text="Items Within Package").grid(row=5, column=0)
        self.items_consumed_entry = tk.Entry(package_edit_create_frame, textvariable=self.items_consumed)
        self.items_consumed_entry.grid(row=5, column=1)

        self.activeflag = tk.StringVar()
        tk.Label(package_edit_create_frame, text="Active Flag").grid(row=6, column=0)
        self.activeflag_entry = tk.Entry(package_edit_create_frame, textvariable=self.activeflag)
        self.activeflag_entry.grid(row=6, column=1)

        # entrys / combobox
        self.package_edit_combobox = ttk.Combobox(package_edit_create_frame, values=self.package_list)
        self.package_edit_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

        self.check_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(package_edit_create_frame, text="Edit Record", variable=self.check_var)
        self.checkbox.grid(row=1, column=4)

        get_package_data = tk.Button(package_edit_create_frame, text="Get Package Data", command=self.get_package_edit_create)
        get_package_data.grid(row=0, column=4)

        update_package_data = tk.Button(package_edit_create_frame, text="Update/Create Package Data", command=lambda: self.get_package_edit_create(True))
        update_package_data.grid(row=7, column=4)

        # format frame widgets
        for widget in package_edit_create_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return package_edit_create_frame

    def get_package_info(self) -> tuple[bool, str | None]:
        """
        get package information from dropdown combobox selector

        return bool for success and errorstring (whereapplic)
        """
        try:
            conn = None

            # get the part_id from search/selector
            dropdown_checker = self.package_combobox.get()

            if dropdown_checker != '':
                self.package_id = dropdown_checker[0:7]                           

            # db connection & sql script get
            conn = uf.get_database_connection()
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

                    self.package_edit_combobox['values'] = self.package_list
                    self.package_edit_combobox.set('')  
                
                # get package info from searcher dropdown                
                if i == 2 and dropdown_checker != '':

                    package_info = conn.query(sql, (self.package_id,))

                    # if data found for search/item selector, update self data
                    if package_info[1]:
                        rows = package_info[1]

                        if rows:
                            (
                                package_id,
                                package_name,
                                description,
                                items_consumed,
                                active_flag,
                            ) = rows[0]

                        # update edit/creation frame if true
                        # default = false, and Package Info frame updated
                        self.package_id_var.set(package_id)
                        self.package_name_var.set(package_name)
                        self.description_var.set(description)
                        self.items_consumed_var.set(items_consumed)

                        if active_flag == 1:
                            self.activeflag_var.set("Active")
                        else:
                            self.activeflag_var.set("Inactive")

                # get part_names, for package info dropdown results
                if i == 3 and self.package_id != '-':

                    # cleanup returned data list > str of itm refs
                    cleaned_data = items_consumed.replace("[","").replace("]","").split(",")
                    final_data = ",".join(f"'{item}'" for item in cleaned_data)

                    # get list of item names
                    data = conn.query(sql.replace("replace1",final_data), ())
                    
                    if data[1]:
                        # join returned data into cleaned string
                        cleaned_data = ",".join(f"'{item[0]}'" for item in data[1])
                        
                        # combine returned list
                        self.items_consumed_var.set(cleaned_data)
    
                    else:
                        # data not found for input
                        self.items_consumed_var.set('*No Items within Package*')

                    # clear user input
                    self.package_combobox.set('') 
                    self.package_id = '-'
                    

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

    def get_package_edit_create(self, action=False) -> tuple[bool, str | None]:
        """
        get package information from dropdown combobox selector
        action = False by default. If True, then edit/create requested by user

        return bool for success and errorstring (whereapplic)
        """
        try:
            conn = None

            # get the part_id from search/selector
            dropdown_checker = self.package_edit_combobox.get()

            if dropdown_checker != '':
                self.package_id = dropdown_checker[0:7]                           

                # check the edit box
                self.check_var.set(True)

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("package_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next package_id
                if i == 0:
                    self.next_package_id = conn.query(sql, ())
                
                # get package info from searcher dropdown                
                if i == 2 and dropdown_checker != '':

                    package_info = conn.query(sql, (self.package_id,))

                    # cleanup previous inputs
                    self.package_id_var_f3.set("-")
                    self.package_name_entry.delete(0, tk.END)
                    self.description_entry.delete(0, tk.END)
                    self.items_consumed_entry.delete(0, tk.END)
                    self.activeflag_entry.delete(0, tk.END)

                    # if data found for search/item selector, update self data
                    if package_info[1]:
                        rows = package_info[1]

                        if rows:
                            (
                                package_id,
                                package_name,
                                description,
                                items_consumed,
                                active_flag,
                            ) = rows[0]

                        # update edit/creation frame if true
                        # default = false, and Package Info frame updated
                        cleaned_items_consumed = items_consumed.replace("[","").replace("]","")

                        self.package_id_var_f3.set(package_id)
                        self.package_name_entry.insert(0, package_name)
                        self.description_entry.insert(0, description)
                        self.items_consumed_entry.insert(0, cleaned_items_consumed)

                        if active_flag == 1:
                            self.activeflag_entry.insert(0, "Active")
                        else:
                            self.activeflag_entry.insert(0, "Inactive")
                        
                        # cleanup comobox
                        self.package_edit_combobox.set('')

                # update existing record
                # action = True button pressed by user
                if i == 4 and action:

                    # get user input params
                    package_id = self.package_id_var_f3.get()
                    package_name = self.package_name_entry.get()
                    description = self.description_entry.get()
                    items_consumed = self.items_consumed_entry.get()
                    active_flag = self.activeflag_entry.get()

                    if active_flag == "Active":
                        active_flag = 1
                    if active_flag == "Inactive":
                        active_flag = 0

                    variable_list = [
                        package_name,
                        description,
                        items_consumed,
                        active_flag
                    ]

                    # check for user inputs into all boxes
                    # errorhandling & msg to user within def
                    results = self.check_user_inputs(variable_list, active_flag, items_consumed)
                    
                    if results[0]: 

                        # check the edit box
                        state = self.check_var.get()

                        if state:
                            # edit enabled
                            items_consumed = str("[" + items_consumed + "]")
                            conn.update(sql, (package_name, description, items_consumed, active_flag, package_id))

                            messagebox.showinfo("Show Info",f"Item {package_name} has been updated")

                # create new existing record
                # action = True button pressed by user
                if i == 5 and action:

                    # check the edit box is unticket (thus create new record)
                    state = self.check_var.get()
                    if not state:

                        items_consumed = str("[" + items_consumed + "]")
                        conn.insert(sql, (self.next_package_id[1][0][0], package_name, description, items_consumed, active_flag))

                    messagebox.showinfo("Show Info",f"New item {self.next_package_id[1][0][0]} , {package_name} has been created")

                    # cleanup previous inputs
                    self.package_id_var_f3.set("-")
                    self.package_name_entry.delete(0, tk.END)
                    self.description_entry.delete(0, tk.END)
                    self.items_consumed_entry.delete(0, tk.END)
                    self.activeflag_entry.delete(0, tk.END)
                    self.check_var.set(False)

            # commit & close
            conn.close(True)            

            # get update to dropdowns
            self.get_package_info()

            return True
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)
        
    def check_user_inputs(self, variable_list: list, active_flag: str, items_consumed: str) -> tuple[bool, str | None]:
        """
        check user inputs for the create/edit boxes within frame 3 
        Return True, or False for sucess with errorstring (where applic)
        """

        try:
            # check for user inputs into all boxes
            # any missing values error to user
            if any(not var for var in variable_list):
                messagebox.showerror("Show Error","Please ensure all boxes are populated. If no items consumed, input 'N/A'.")
                raise ValueError("Missing data within inputs")
            
            # check active_flag = Active/Inactive
            if active_flag not in [1,0]:
                messagebox.showerror("Show Error","Please ensure Active flag is 'Active' or 'Inactive'.")
                raise ValueError("Active Flag data incorrect. Needs to be  ['Active','Inactive']")

            # check only string data input, i.e. 123 not accepted
            if type(items_consumed) != str:                
                messagebox.showerror("Show Error",'Input data is a number, required is "N/A" or "ITM-001,ITM002..." etc or for single item "ITM-001"')
                raise ValueError("Input incorrect, not a string or 'N/A'")

            # check item consumed input to match ITM-*** or "N/A"
            result = self.validate_itm_list(items_consumed)

            if not result:
                messagebox.showerror("Show Error",'Input data is not correct format. "N/A" or "ITM-001,ITM002..." etc or for single item "ITM-001"')
                raise ValueError("Input incorrect, 'N/A' or ITM list")
            

            return True, None
        
        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return False, str(err)

    def validate_itm_list(self, text: str) -> bool:
        """
        validate the ITM values within list
        Regex: ^ start str, (,)ITM-/ is literal, /d{3} is expecting 3 digits, *means 0 or more elements
        """
        import re

        # if noting input
        if "N/A" in text:
            return True

        # validate user input
        parts = [p.strip() for p in text.split(",")]
        return all(re.fullmatch(r"ITM-\d{3}", p) for p in parts)