import main_window as mw
import utility_functions as uf

# TODO: Booking tab
    # - create
    # - add new booking
    # - amend / cancel existing booking
    # - add finance SQL view & window

# TODO: triggers


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
        test_login = ["USR-002","CUS_USR"]
        main_win = mw.Main(test_login[0],test_login[1])
        result = main_win.run()

    else: 
        
        import xml_functions as xfc

        filepath = "C:/Users/eliot/Downloads/access_codes.xml"
        result = xfc.database_updater_from_xml(filepath)

        print(result)
