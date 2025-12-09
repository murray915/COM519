import main_window as mw
import utility_functions as uf

# TODO: admin tab
    # - xml import/export
    # - application settings

# TODO: Booking tab
    # - create
    # - add new booking
    # - amend / cancel existing booking
    # - add finance SQL view & window

# TODO: xml
# TODO: triggers


##### IF I HAVE TIME #####
# TODO:
    # Add image to garage
    # add image to account

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
        pass



