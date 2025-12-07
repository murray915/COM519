from icecream import ic
import login_window as lw
import main_window as mw
import utility_functions as uf
import image_functions as ifc
import csv



# TODO: fix phone number insert/recovery



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


        # conn = uf.get_database_connection()
        # sql = uf.load_sql_file("customer_scripts.sql")
        # sql_statements = sql.replace("\n", "").split(";")

        # for i, sql in enumerate(sql_statements):

        #     if i == 0:
        #         veh_id = conn.query(sql, ())
        #         next_veh_id = veh_id[1][0][0]
                
        # conn.close()