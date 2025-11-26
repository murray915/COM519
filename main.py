from icecream import ic
from login_window import *
from main_window import *


if __name__ == "__main__":
    Login_process = Login_Window()
    result = Login_process.run()

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