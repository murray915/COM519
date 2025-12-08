from icecream import ic
import login_window as lw
import main_window as mw
import utility_functions as uf
import image_functions as ifc
import csv


# TODO: admin tab
    # = create
    # - password updates
    # - access code update
    # - xml import/export
    # - application settings

# TODO: account tab
    # - create
    # - add membership add to account tab

# TODO: Booking tab
    # - create
    # - add new booking
    # - amend / cancel existing booking
    # - add finance SQL view & window

# TODO: xml
# TODO: triggers

if __name__ == "__main__":
    
    # # login window
    # Login_process = lw.Login_Window()
    # result = Login_process.run()

    # # login completed 
    # # main
    # if result:
    #     main_win = mw.Main(result[0],result[1])
    #     result = main_win.run()

    hello = True

    if hello:        
        test_login = ["USR-005","CUS_USR"]
        main_win = mw.Main(test_login[0],test_login[1])
        result = main_win.run()

    else: 
        pass
