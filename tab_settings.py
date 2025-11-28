import tkinter as tk
import icecream as ic
import utility_functions as uf
from tkinter import ttk

class Tab3(ttk.Frame):
    def __init__(self, parent, curr_user):
        super().__init__(parent)

        self.curr_user = curr_user
        self.tab_name = "Stock"

        self.part_id = "ITM-001"
        self.name = None
        self.description = None
        self.common_repair_group = None
        self.image = None
        self.active_flag = None

        self.stock_level = None
        self.list_part_ids = None
        
        self.get_stock_item_info()

        ttk.Label(self, text="This is Tab 3").pack(pady=20)

        # general params
        self.frame = tk.Frame(self)
        self.frame.pack()

        # frame 1 - Item Info
        item_info_frame = tk.LabelFrame(self.frame, text="Item Information")
        item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        tk.Label(item_info_frame, text=self.description).grid(row=0, column=0)
        tk.Label(item_info_frame, text=self.active_flag).grid(row=1, column=0)


        # format frame widgets
        for widget in item_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)


        # frame 2 - Item Creation
        # item_info_frame = tk.LabelFrame(self.frame, text="Item Information")
        # item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


        # frame 3 - Stock Info
        item_info_frame = tk.LabelFrame(self.frame, text="Stock Information")
        item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)


        # frame 4 - Display Chart orders. Y = Date, X = QTY
        item_info_frame = tk.LabelFrame(self.frame, text="Stock Consumption Graphics")
        item_info_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        ttk.Button(self,text='Get Item Data',command=self.get_stock_item_info).pack(expand=True)

    def get_stock_item_info(self) -> tuple[bool, str | None]:
        """
        get stock information from part_id selector

        return bool for success and errorstring (whereapplic)
        """

        try:

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("stock_data_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):

                # get data
                if i == 0:
                    part_info = conn.query(sql, (self.part_id,))

            # if data found, update self data
            if part_info:
                self.part_id = part_info[1][0][0]
                self.name = part_info[1][0][1]
                self.description = part_info[1][0][2]
                self.common_repair_group = part_info[1][0][3]
                self.image = part_info[1][0][4]
                self.active_flag = part_info[1][0][5]
            
            # data not found err back
            else:
                conn.close()
                raise ValueError(f"No data found for part_id {self.part_id}")

            # commit & close
            conn.close(True)
        
            return True
    
        except Exception as err:
            ic(f"Unexpected error: {err}, type={type(err)}")
            conn.close()
            return False, str(err)
