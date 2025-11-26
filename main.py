from icecream import ic
import login_window as lw
import main_window as mw


if __name__ == "__main__":
    
    # # login window
    # Login_process = lw.Login_Window()
    # result = Login_process.run()

    # # login completed 
    # # main
    # if result:
    #     main_win = mw.Main(result[0],result[1])
    #     result = main_win.run()


    test_login = ["USR-001","CUS_USR"]
    main_win = mw.Main(test_login[0],test_login[1])
    result = main_win.run()

    # Login_process = Login_Window()
    # data = Login_process.encryption("123", True)

    # db = uf.get_database_connection()
    # value_username = '123'
    # value_password = data

    # ic(value_username, value_password)

    # sql = 'UPDATE login_details SET password = ? WHERE user_id = "USR-001"'
    # db.update(sql, (value_password,))
    # db.commit()
    # db.close()