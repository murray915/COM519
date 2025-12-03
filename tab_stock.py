import tkinter as tk
import icecream as ic
import utility_functions as uf
import image_functions as ifc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import pandas as pd
import os
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Tab3(ttk.Frame):
    def __init__(self, parent, curr_user):
        super().__init__(parent)

        self.curr_user = curr_user
        self.tab_name = "Stock"

        self.part_id = '-'
        self.name = '-'
        self.description = '-'
        self.common_repair_group = '-'
        self.image = None
        self.active_flag = '-'

        self.stock_level = None
        self.list_part_ids = None
        self.searchkey = None
        self.image_var = None

        ttk.Label(self, text="This is the Item Management Tab" \
        "\n> To view items in the top frame, please select the ITM reference from the dropdown or search using the search bar, then press 'Get Item Data'." \
        "\n> To create new items input the name, description and Common Repair Group, and 'create item', once created an image can be uploaded using the newly created item record" \
        "\n> To upload image, input the ITM number of an item. Select png/jpg filetype and press the button to start the folderwindow to select the file" \
        "\n\n> Below the item create/show the Current stock Information is shown, and allow increasing current stock. Primary Garage for user taken as default" \
        "\n> The third frame will display recent demands for the selected item, bookings by week"
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

        btn = ttk.Button(self.frame, text="Refresh Plot", command=self.refresh_frame_3)
        btn.grid(row=2, column=1)

        # frame 3 - Stock Info
        #item_info_frame = tk.LabelFrame(self.frame, text="Stock Information")
        #item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # frame 4 - Display Chart orders. Y = Date, X = QTY
        #item_info_frame = tk.LabelFrame(self.frame, text="Stock Consumption Graphics")
        #item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


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

        get_data_button = ttk.Button(item_info_frame,text='Get Item Data',command=self.get_stock_item_info)
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
            item_comsumption_graph_frame.grid(row=1, column=1, columnspan=10, padx=10, pady=10)
    
            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("stock_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get specific item_id data
                if i == 5:       
                    data = conn.query(sql, ())

            # create csv for data
            with open('./data/temp.csv', 'w', newline='') as fp:
                myFile = csv.writer(fp)
                myFile.writerow(data[0])
                
                # add data into csv
                for i in data[1]:
                    myFile.writerow(i)
            
            # csv params
            fp_file = './data/temp.csv'
            fp = pd.read_csv('./data/temp.csv')

            # plot titles
            pivot = fp.pivot_table(
                index="year_month",
                columns="part_id",
                values="qty_consumed",
                aggfunc="sum"
            )

            # plt & ktinker params
            fig, ax = plt.subplots(figsize=(8, 4))
            pivot.plot(ax=ax, marker="o")

            # graph params
            ax.set_title("Itm Consumption per Part (by Month)")
            ax.set_xlabel("Year-Month")
            ax.set_ylabel("Qty Consumed")
            plt.setp(ax.get_xticklabels(), rotation=45)
            fig.tight_layout()
            #plt.show()

            # create canvas & plot graph
            canvas = FigureCanvasTkAgg(fig, master=item_comsumption_graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            # delete temp png file
            if os.path.exists(fp_file):
                os.remove(fp_file) 

            return True, None

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)
    

    def refresh_frame_3(self):
        """
        Refresh data in frame 3. destroy and recreate
        
        :param self: Description
        :return: Description
        :rtype: type[bool]
        """
        try:
            # Destroy if it already exists
            if hasattr(self, "item_image_upload_frame") and self.item_comsumption_graph_frame is not None:
                self.item_comsumption_graph_frame.destroy()

            # Recreate new frame
            self.item_comsumption_graph_frame = self.frame_3()

            btn = ttk.Button(self.frame, text="Refresh Plot", command=self.refresh_frame_3)
            btn.grid(row=2, column=1)

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            return False, str(err)
        
        
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
                
                    # if data found for search/item selector, update self data
                    if part_info[1]:
                        self.partid_var.set(part_info[1][0][0])
                        self.name_var.set(part_info[1][0][1])
                        self.description_var.set(part_info[1][0][2])
                        self.commongroup_var.set(part_info[1][0][3])
                        self.image = part_info[1][0][4]   

                        if part_info[1][0][5] == 1:
                            self.activeflag_var.set("Active")
                        else:
                            self.activeflag_var.set("Inactive")

                        self.image = ifc.get_tk_image_from_db(self.part_id)

                        if self.image is not None:

                            self.image_label.config(image=self.image)
                            self.image_label.image = self.image
                    
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

            if "jpg" in filepath:
                output = ifc.upload_jpg_files_to_db(self.image_item_id.get(), filepath)
            else: 
                output = ifc.upload_tk_image_to_db(self.image_item_id.get(), filepath)

            if type(output) == tuple:
                raise ValueError(output[1])

            messagebox.showinfo("show info",f"Item image uploaded successfully to {self.image_item_id.get()}")

            return True

        except Exception as err: # Exception Block. Return data to user & False
            print(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
            return False, str(err)