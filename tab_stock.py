import tkinter as tk
import icecream as ic
import utility_functions as uf
import image_functions as ifc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Tab3(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.prime_garage = uf.validate_primary_garage_id(curr_user, True)
        self.tab_name = "Stock"
        self.controller = controller

        self.part_id = '-'
        self.name = '-'
        self.description = '-'
        self.common_repair_group = '-'
        self.image = None
        self.active_flag = '-'

        self.stock_part_id = '-'
        self.stock_garage_id = '-'
        self.stock_name = '-'
        self.stock_description = '-'
        self.stock_common_repair_group = '-'
        self.stock_new_level = '-'
        self.stock_current_level = 0

        self.stock_level = None
        self.list_part_ids = None
        self.list_garage_ids = None
        self.searchkey = None
        self.image_var = None

        ttk.Label(self, text="This is the Item Management Tab" \
        "\n> To view items in the top frame, please select the ITM reference from the dropdown or search using the search bar, then press 'Get Item Data'." \
        "\n> To create new items input the name, description and Common Repair Group, and 'create item', once created an image can be uploaded using the newly created item record" \
        "\n> To upload image, input the ITM number of an item. Select png/jpg filetype and press the button to start the folderwindow to select the file" \
        "\n\n> Below the item create/show the Current stock Information is shown, and allow increasing current stock. Select a Garage and Item, then press update when the correct details are displayed." \
        "\n> The final frame displays all the items consumed by month, across all garages"
        ).pack(pady=20)

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Item Info
        # row 0, col 0
        self.item_info_frame = self.frame_1()

        # frame 2 - Item Creation
        # row 0, col 5
        self.item_creation_frame = self.frame_2()

        # frame 3 - Item Image Upload
        # row 1, col 5
        self.item_comsumption_graph_frame = self.frame_3()

        # frame 4 - Stock Info
        # row 2, col 0
        self.Stock_Info_and_update = self.frame_4()
        
        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)

    def frame_1(self) -> object:
        """
        constructor for frame 1 : item_info_frame
        """

        item_info_frame = tk.LabelFrame(self.frame, text="Item Information")
        item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
        # Labels
        tk.Label(item_info_frame, text="Search :").grid(row=0, column=0)
        tk.Label(item_info_frame, text="Dropdown List for Items :").grid(row=1, column=0)

        self.partid_var = tk.StringVar(value=self.part_id)
        tk.Label(item_info_frame, text="Item ID").grid(row=2, column=0)
        tk.Label(item_info_frame, textvariable=self.partid_var).grid(row=2, column=1)

        self.name_var = tk.StringVar(value=self.name)
        tk.Label(item_info_frame, text="Item Name").grid(row=3, column=0)
        tk.Label(item_info_frame, textvariable=self.name_var).grid(row=3, column=1)

        self.description_var = tk.StringVar(value=self.description)
        tk.Label(item_info_frame, text="Item Description").grid(row=4, column=0)
        tk.Label(item_info_frame, textvariable=self.description_var).grid(row=4, column=1)

        self.commongroup_var = tk.StringVar(value=self.common_repair_group)
        tk.Label(item_info_frame, text="Common Repair Group").grid(row=5, column=0)
        tk.Label(item_info_frame, textvariable=self.commongroup_var).grid(row=5, column=1)

        self.activeflag_var = tk.StringVar(value=self.active_flag)
        tk.Label(item_info_frame, text="Active Flag").grid(row=6, column=0)
        tk.Label(item_info_frame, textvariable=self.activeflag_var).grid(row=6, column=1)
        
        if not hasattr(self, "image_label"):
            self.image_label = tk.Label(item_info_frame, image=self.image)
            self.image_label.grid(row=2, column=3, rowspan=3, padx=10, pady=10)
        else:
            self.image_label.config(image=self.image)
            self.image_label.image = self.image

        # entrys / combobox
        self.searchkey = tk.StringVar()
        self.searchkey_entry = tk.Entry(item_info_frame, textvariable=self.searchkey)
        self.searchkey_entry.grid(row=0, column=1)

        get_data_button = tk.Button(item_info_frame,text='Get Item Data',command=self.get_stock_item_info)
        get_data_button.grid(row=0, column=2)
        
        self.item_combobox = ttk.Combobox(item_info_frame, values=self.list_part_ids)
        self.item_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

        self.get_stock_item_info()

        # format frame widgets
        for widget in item_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return item_info_frame

    def frame_2(self) -> object:
        """
        constructor for frame 2 : item_creatiom_frame
        """

        item_creation_frame = tk.LabelFrame(self.frame, text="Item Creation")
        item_creation_frame.grid(row=0, column=5, columnspan=5, padx=10, pady=10)
 
        # frame get data
        # labels        
        tk.Label(item_creation_frame, text="Item Name").grid(row=0, column=0)
        tk.Label(item_creation_frame, text="Item Description").grid(row=1, column=0)
        tk.Label(item_creation_frame, text="Common Repair Group").grid(row=2, column=0)
        tk.Label(item_creation_frame, text="").grid(row=3, column=0)
        tk.Label(item_creation_frame, text="Item ID").grid(row=4, column=0)
        tk.Label(item_creation_frame, text="Image File Type").grid(row=5, column=0)

        # varibles
        self.new_item_name = tk.StringVar()
        self.new_item_des = tk.StringVar()
        self.new_item_comm_group = tk.StringVar()
        self.image_item_id = tk.StringVar()

        # entrys
        self.username_entry = tk.Entry(item_creation_frame, textvariable=self.new_item_name)
        self.username_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(item_creation_frame, textvariable=self.new_item_des)
        self.password_entry.grid(row=1, column=1)
        self.password_entry = tk.Entry(item_creation_frame, textvariable=self.new_item_comm_group)
        self.password_entry.grid(row=2, column=1)  
        self.image_item_id_entry = tk.Entry(item_creation_frame, textvariable=self.image_item_id)
        self.image_item_id_entry.grid(row=4, column=1)

        self.item_combobox_filetypes = ttk.Combobox(item_creation_frame, values=["","png","jpg"])
        self.item_combobox_filetypes.grid(row=5, column=1, columnspan=3, sticky="ew")

        get_data_button = tk.Button(item_creation_frame,text='Create Item',command=self.create_new_item)
        get_data_button.grid(row=3, column=4)

        upload_png_button = tk.Button(item_creation_frame, text="Upload image file", command=self.select_file)
        upload_png_button.grid(row=6, column=4)

        # format frame widgets
        for widget in item_creation_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        return item_creation_frame

    def frame_3(self) -> tuple[object, str | None]:
        """
        constructor for frame 3 : item_comsumption_graph_frame
        """
        try:
            conn = None

            item_comsumption_graph_frame = tk.LabelFrame(self.frame, text="Item Consumption Data")
            item_comsumption_graph_frame.grid(row=1, column=6, columnspan=10, padx=10, pady=10)
    
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("stock_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get specific item_id data
                if i == 5:       
                    data = conn.query(sql, ())

            fig = uf.build_matplot_objects_stocktab(data, "Item Consumption per Part (by Month)","Year-Month","Qty Consumed","part_id","qty_consumed")

            # create canvas & plot graph
            canvas = FigureCanvasTkAgg(fig, master=item_comsumption_graph_frame)
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

    def frame_4(self) -> tuple[object, str | None]:
        """
        constructor for frame 4 : Stock_Info_and_update
        
        """
        try:
            conn = None

            Stock_Info_and_update = tk.LabelFrame(self.frame, text="Stock Information & Update")
            Stock_Info_and_update.grid(row=1, column=0, columnspan=5, padx=10, pady=10)
    
            # frame get data 
            # Labels & variable
            tk.Label(Stock_Info_and_update, text="Dropdown List for Items :").grid(row=0, column=0)
            tk.Label(Stock_Info_and_update, text="Dropdown List for Garages :").grid(row=1, column=0)

            self.stock_partid_var = tk.StringVar(value=self.stock_part_id)
            tk.Label(Stock_Info_and_update, text="Item ID").grid(row=2, column=0)
            tk.Label(Stock_Info_and_update, textvariable=self.stock_partid_var).grid(row=2, column=1)

            self.stock_garageid_var = tk.StringVar(value=self.stock_garage_id)
            tk.Label(Stock_Info_and_update, text="Garage ID").grid(row=3, column=0)
            tk.Label(Stock_Info_and_update, textvariable=self.stock_garageid_var).grid(row=3, column=1)

            self.stock_name_var = tk.StringVar(value=self.stock_name)
            tk.Label(Stock_Info_and_update, text="Item Name").grid(row=4, column=0)
            tk.Label(Stock_Info_and_update, textvariable=self.stock_name_var).grid(row=4, column=1)

            self.stock_description_var = tk.StringVar(value=self.stock_description)
            tk.Label(Stock_Info_and_update, text="Item Description").grid(row=5, column=0)
            tk.Label(Stock_Info_and_update, textvariable=self.stock_description_var).grid(row=5, column=1)
            
            self.stock_current_level_var = tk.StringVar(value=self.stock_current_level)
            tk.Label(Stock_Info_and_update, text="Current Stock level").grid(row=6, column=0)
            tk.Label(Stock_Info_and_update, textvariable=self.stock_current_level_var).grid(row=6, column=1)
            
            self.stock_new_level = tk.StringVar()
            tk.Label(Stock_Info_and_update, text="New Stock Level").grid(row=7, column=0)
            self.stock_new_level_entry = tk.Entry(Stock_Info_and_update, textvariable=self.stock_new_level)
            self.stock_new_level_entry.grid(row=7, column=1)

            # entrys
            self.stock_item_combobox = ttk.Combobox(Stock_Info_and_update, values=self.list_part_ids)
            self.stock_item_combobox.grid(row=0, column=1, columnspan=3, sticky="ew")

            self.item_combobox_garages = ttk.Combobox(Stock_Info_and_update, values=self.list_garage_ids)
            self.item_combobox_garages.grid(row=1, column=1, columnspan=3, sticky="ew")
            
            update_item_data = tk.Button(Stock_Info_and_update, text="Get Item/Stock Data", command=self.get_stock_garage_info)
            update_item_data.grid(row=0, column=4)

            upload_png_button = tk.Button(Stock_Info_and_update, text="Update Stock Level", command=self.get_stock_garage_info)
            upload_png_button.grid(row=6, column=4)

            self.get_stock_garage_info()

            # format frame widgets
            for widget in Stock_Info_and_update.winfo_children():
                widget.grid_configure(padx=10, pady=5)

            return Stock_Info_and_update      
          

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

    def on_show(self):
        """Called whenever this tab becomes active"""
        print("Refreshing Tab data")
        self.get_stock_item_info()
        self.get_stock_garage_info()

    def get_stock_item_info(self) -> tuple[bool, str | None]:
        """
        get stock information from part_id selector

        return bool for success and errorstring (whereapplic)
        """

        try:
            conn = None

            # get the part_id from search/selector
            #self.part_id = self.searchkey_entry.get()
            searchley_checker = self.searchkey_entry.get()
            dropdown_checker = self.item_combobox.get()

            if searchley_checker != '':
                self.part_id = searchley_checker

            elif dropdown_checker != '':
                cleaned_value = dropdown_checker[0:7]
                self.part_id = cleaned_value

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("stock_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get specific item_id data
                if i == 0 and self.part_id != '':
                    part_info = conn.query(sql, (self.part_id,))
                
                    # if data found for search/item selector, update self data refs
                    if part_info[1]:
                        rows = part_info[1]

                        # confirm data found & update
                        if rows:
                            (
                                partid,
                                name,
                                description,
                                commongroup,
                                image,
                                activeflag
                            ) = rows[0]

                        # set self vars to display in application
                        self.partid_var.set(partid)
                        self.name_var.set(name)
                        self.description_var.set(description)
                        self.commongroup_var.set(commongroup)
                        self.image = image

                        # convert bool > display text
                        if activeflag == 1:
                            self.activeflag_var.set("Active")
                        else:
                            self.activeflag_var.set("Inactive")

                        # check if image returned data is emtpy
                        # if value found, pull blob data & update self.image with tk_image obj
                        if self.image is not None:
                            self.image = ifc.get_tk_image_from_db(self.part_id) # get obj
                            self.image_label.config(image=self.image) #configure variable & image
                            self.image_label.image = self.image # assign to image to label

                        # no image for item, unassign vars & config blank
                        else:
                            self.image = None
                            self.image_label.config(image="")
                            self.image_label.image = None

                    # error message for nonfound searches
                    elif self.part_id != '-':
                        messagebox.showinfo("Search Error", 
                                            'No item found for the input value. ' \
                                            '\nPlease check the item id is correct or use the dropdown')
                    
                    # clear user input
                    self.searchkey.set('')

                # get all item_ids for dropdown
                if i == 1:
                    all_item_data = conn.query(sql, ())

                    if all_item_data:
                        output_list = []

                        # clean data intp list
                        for i in all_item_data[1]:
                            output_list.append(i[0])
                        
                        # add to self var
                        self.list_part_ids = output_list
            
                    # reset the combobox list on datarefresh
                    self.item_combobox['values'] = self.list_part_ids
                    self.item_combobox.set('')

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

    def get_stock_garage_info(self) -> tuple[bool, str | None]:
        """
        get garage/item Stock information from inputs into frame_4

        return bool for success and errorstring (whereapplic)
        """

        try:
            # set general params
            conn = None
            garage_id = None
            part_id = None

            # get user input params
            dropdown_checker_garage = self.item_combobox_garages.get()
            dropdown_checker_item = self.stock_item_combobox.get()
            new_stock_input = self.stock_new_level_entry.get()

            # check for user inputs into all boxes
            # only search OR update can be enacted
            if (dropdown_checker_garage != '' or dropdown_checker_item != '') and new_stock_input != '':
                messagebox.showerror("Show Error","Please only search or update currently selected stock.")
                raise ValueError("Search vs Update conflict")
            
            if (dropdown_checker_garage == '' and dropdown_checker_item != '') or dropdown_checker_garage != '' and dropdown_checker_item == '':
                messagebox.showerror("Show Error","Only one of the required inputs completed. Please ensure garage and items are selected. If no Garage is selectable, please ensure primary garage is input into your account")
                self.item_combobox_garages.set('')
                self.stock_item_combobox.set('')
                raise ValueError("Search input failure.")
                        
            # get the part_id from search/selector
            if dropdown_checker_garage != '':
                cleaned_value = dropdown_checker_garage[0:8]
                garage_id = cleaned_value.replace("-","_")

            if dropdown_checker_item != '':
                cleaned_value = dropdown_checker_item[0:7]
                part_id = cleaned_value

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("garage_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get specific item_id data
                if i == 0:
                    next_garage_id = conn.query(sql, ())
                    next_garage_id = next_garage_id[1][0][0]

                # get all garage_id data for dropdown
                if i == 1:
                    all_garage_data = conn.query(sql, ())

                    if all_garage_data:
                        output_list = []
                        temp_output_list = []

                        # clean data intp list
                        for i in all_garage_data[1]:
                            temp_output_list.append(i[0])
                        
                        # add to self var, remove all non-prime garages
                        if self.prime_garage == 'N/A':
                            self.list_garage_ids = None
                        else:

                            # add to output list only primary garage
                            for i in temp_output_list:
                                sub = i[0:8]

                                if sub == self.prime_garage:
                                    output_list.append(i)

                            # update self var
                            self.list_garage_ids = output_list
            
                    # reset the combobox list on datarefresh
                    self.item_combobox_garages['values'] = self.list_garage_ids
                    self.item_combobox_garages.set('')


                # get stock levels for garage_id & item_id
                if i == 2 and (dropdown_checker_garage != '' and dropdown_checker_item != ''):
                    
                    # search params
                    sql_garage_id = f'stocklevel_{garage_id}'
                    sql = sql.replace("replace1", sql_garage_id)
                    data = conn.query(sql, (part_id,))

                    # if data found for search/item selector, update self data
                    if data[1]:
                        rows = data[1]

                        if rows:
                            (
                                partid,
                                name,
                                description,
                                curr_lvl
                            ) = rows[0]

                        self.stock_partid_var.set(partid)
                        self.stock_name_var.set(name)
                        self.stock_description_var.set(description)
                        self.stock_current_level_var.set(curr_lvl)

                        self.stock_garageid_var.set(dropdown_checker_garage[0:8])

                    self.stock_item_combobox.set('')

                if i == 3 and new_stock_input != '' and (dropdown_checker_garage == '' and dropdown_checker_item == ''): 
                    
                    # check user input
                    if not uf.is_nonnegative_whole_number(new_stock_input):
                        messagebox.showerror("Show Error","New Stock input has to be a positive numeric value. Please ensure input is a whole number, of 0 or above.")
                        raise ValueError("User input numeric failure.")
                    
                    # search params
                    garage_id = self.stock_garageid_var.get()
                    sql_garage_id = f'stocklevel_{garage_id.replace("-","_")}'             
                    sql = sql.replace("replace1", sql_garage_id)
                    conn.update(sql, (self.stock_new_level_entry.get(),self.stock_partid_var.get()))

                    messagebox.showinfo("Show Info",f"Stock Level updated for item {self.stock_partid_var.get()}, for garage {garage_id} ")

                    self.stock_new_level.set('')
                    self.stock_partid_var.set('-')
                    self.stock_name_var.set('-')
                    self.stock_description_var.set('-')
                    self.stock_current_level_var.set('-')
                    self.stock_garageid_var.set('-')
                    

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

    def create_new_item(self, create=True) -> tuple[bool, str | None]:
        """
        create new item, get data from userinput frame_2
        create default True, if testing, pass False
        return True/False and errorstring (where applic.)
        """
        try:
            conn = None

            # check user input values
            if self.new_item_name.get() == '' or self.new_item_des.get() == '' or self.new_item_comm_group.get() == '':
                messagebox.showerror("show info","Missing Data in Item Create boxes")
                raise ValueError("Missing Data in Item Create boxes")

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("stock_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")

            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get next id
                if i == 3:
                    next_id = conn.query(sql, ())
                    next_id = next_id[1][0][0]

                # get all table names
                if i == 2:
                    data = conn.query(sql, ())

                # get all table names
                if i == 4:
                    insert_sql = sql

                    # make str from sql table names
                    output_str = []
                    output_list = []

                    for i in data[1]:
                        output_str.append(i[1])

                    # make str of ? for insert
                    for i in range(len(data[1])):
                        output_list.append("?")

                    insert_sql = insert_sql.replace("replace1",", ".join(output_str)).replace("replace2",", ".join(output_list))

            insert_values = [
                next_id, 
                self.new_item_name.get().strip(),
                self.new_item_des.get().strip(),
                self.new_item_comm_group.get().strip(),
                None,
                1
                ]

            while len(insert_values) < len(data[1]):
                insert_values.append(0)

            insert_sql = insert_sql.replace("replace1",", ".join(output_str)).replace("replace2",", ".join(output_list))
            conn.insert(insert_sql, tuple(insert_values))

            # commit records (false=testing)
            # close db connection
            if create:
                conn.commit()

            sql = f"SELECT * FROM STOCK WHERE part_id = '{next_id}'"
            data = conn.query(sql, ())

            if not data:
                messagebox.showerror("Show Info","Failed Item Creation")
                raise ValueError("Failed Item Creation")
            else:
                messagebox.showinfo("Show Info",f"Item Created Successfully new reference: {next_id}")

            conn.close()

            # clear data input
            self.new_item_name.set('')
            self.new_item_des.set('') 
            self.new_item_comm_group.set('')

            return True

        except Exception as err: # Exception Block. Return data to user & False
            print(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
            
            if conn:
                conn.close()
            else:
                pass
            
            return False, err

    def select_file(self) -> tuple[bool, str | None]:
        """"
        file selector
        """
        
        try:

            # check user input values
            if self.item_combobox_filetypes.get() == '' or self.image_item_id.get() == '':
                messagebox.showerror("show info","Missing Data in Item image boxes")
                raise ValueError("Missing Data in Item Create boxes")
           
            # get filepath from user
            filepath = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("jpg files", "*.jpg"), ("png files", "*.png")]
            )
            
            # check user filepath values
            if filepath == '' or filepath is None:
                messagebox.showerror("show info","File not selected")
                raise ValueError("No value file selected")                

            self.upload_file = filepath

            output = ifc.upload_image_to_db(self.image_item_id.get(), filepath)

            if not output[0]:
                raise ValueError(output[1])

            messagebox.showinfo("show info",f"Item image uploaded successfully to {self.image_item_id.get()}")

            return True

        except Exception as err: # Exception Block. Return data to user & False
            print(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
            return False, str(err)