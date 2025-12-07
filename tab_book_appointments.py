import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

class Tab2(ttk.Frame):
    def __init__(self, parent, controller, curr_user, style_name):
        super().__init__(parent, style=style_name)

        self.curr_user = curr_user
        self.tab_name = "Book Appointments"
        self.controller = controller
        
        ttk.Label(self, text="This is the Book Appointment Tab" \
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
        #self.item_info_frame = self.frame_1()

        # frame 2 - Item Creation
        # row 0, col 5
        #self.item_creation_frame = self.frame_2()

        # frame 3 - Item Image Upload
        # row 1, col 5
        #self.item_comsumption_graph_frame = self.frame_3()

        # close app button
        close_app_button = tk.Button(self.frame,
                text="Close Application",
                command=self.controller.close_application
        )
        close_app_button.grid(row=3, column=3)


    # def frame_1(self) -> object:
    #     """
    #     constructor for frame 1 : booking_data_user_form
    #     """

    #     booking_data_user_form = tk.LabelFrame(self.frame, text="New Booking Form")
    #     booking_data_user_form.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
 
    #     # Labels
    #     tk.Label(booking_data_user_form, text="Search :").grid(row=0, column=0)
    #     tk.Label(booking_data_user_form, text="Dropdown List for Items :").grid(row=1, column=0)

    #     self.partid_var = tk.StringVar(value=self.part_id)
    #     tk.Label(booking_data_user_form, text="Item ID").grid(row=2, column=0)
    #     tk.Label(booking_data_user_form, textvariable=self.partid_var).grid(row=2, column=1)        

    #     # widgets
    #     # Add Calendar
    #     self.cal = Calendar(self.frame, selectmode = 'day',
    #                 year = 2020, month = 5,
    #                 day = 22)

    #     self.cal.grid(row=0, column=0)

    #     def grad_date():
    #         date.config(text = "Selected Date is: " + cal.get_date())

    #     # entrys / combobox
    #     self.searchkey = tk.StringVar()
    #     self.searchkey_entry = tk.Entry(booking_data_user_form, textvariable=self.searchkey)
    #     self.searchkey_entry.grid(row=0, column=1)

    #     get_data_button = ttk.Button(booking_data_user_form,text='Get Item Data',command=self.get_stock_item_info)
    #     get_data_button.grid(row=0, column=2)
        
    #     self.item_combobox = ttk.Combobox(booking_data_user_form, values=self.list_part_ids)
    #     self.item_combobox.grid(row=1, column=1, columnspan=3, sticky="ew")

    #     # format frame widgets
    #     for widget in booking_data_user_form.winfo_children():
    #         widget.grid_configure(padx=10, pady=5)

    #     return booking_data_user_form
    

    # def grad_date(self):
    #     date.config(text = "Selected Date is: " + self.cal.get_date())