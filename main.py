from icecream import ic
import login_window as lw
import main_window as mw
import utility_functions as uf
import image_functions as ifc
import csv

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
        test_login = ["USR-001","CUS_USR"]
        main_win = mw.Main(test_login[0],test_login[1])
        result = main_win.run()

    else:

        pass