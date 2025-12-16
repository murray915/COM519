import main_window as mw
import utility_functions as uf
import login_window as lw

# TODO: Booking_Staff tab
    # - create
    # - Complete booking


##### ##### ##### ##### ##### 
#####   IF I HAVE TIME  #####
##### ##### ##### ##### #####
 
# TODO:
    # Add image to garage
    # add image to account
    # - xml import (db table type checker)
    # - application settings


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
        #test_login = ["USR-001","CUS_USR"] # user
        test_login = ["USR-015","STF_USR"] # staff
        #test_login = ["USR-016","ADMIN"] # admin
        

        main_win = mw.Main(test_login[0],test_login[1])
        result = main_win.run()

    else:
        data = uf.get_garagelist_details()

        print(data)

        #'Mechanic'