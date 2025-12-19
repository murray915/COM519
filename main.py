import main_window as mw
import utility_functions as uf
import login_window as lw


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
        #test_login = ["USR-015","STF_USR"] # staff
        test_login = ["USR-016","ADMIN"] # admin
        

        main_win = mw.Main(test_login[0],test_login[1])
        result = main_win.run()

    else:

        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("booking_staff_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts
        for i, sql in enumerate(sql_statements):

            # get next transaction id
            if i == 1:
                next_transaction_id = conn.query(sql, ())
                next_transaction_id = next_transaction_id[1][0][0]

            # get table data
            # current open bookings
            if i == 0:
                rows = conn.query(sql, ('GRDG-002',))

        print(rows)

    #     #'Mechanic'