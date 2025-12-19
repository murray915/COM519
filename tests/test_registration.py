import pytest
from .test_fixtures import *
from registration_window import *
from unittest.mock import patch, MagicMock

import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"


def test_info_validation_all_missing_fields():
    """
    Docstring for test_info_validation_all_missing_fields
            Test empty fields input by user into window. Return False/Error back                
    """

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # input nothing into all parameters in window
    win.first_name.set("")
    win.surname_name.set("")
    win.add_1.set("")
    win.add_2.set("")
    win.email_add.set("")
    win.post_code.set("")
    win.phone_no.set("")

    # check user inputs > return true for pass. False if validation fails
    result = win.validate_user_information_data()

    assert any("missing input" in msg for msg in result)


def test_info_validation_some_missing_fields():
    """
    test single empty field > true
    """

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.first_name.set("Test")
    win.surname_name.set("Test")
    win.add_1.set("Test")
    win.add_2.set("")
    win.email_add.set("Test")
    win.post_code.set("000 000")
    win.phone_no.set("123")

    result = win.validate_user_information_data()

    assert any("missing input" in msg for msg in result)


def test_info_validation_valid_fields():
    """
    test valid phone no passed as non-str > true
    """

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.first_name.set("Test")
    win.surname_name.set("Test")
    win.add_1.set("Test")
    win.add_2.set("Test")
    win.email_add.set("Test")
    win.post_code.set("000 000")
    win.phone_no.set(123)

    result = win.validate_user_information_data()

    assert result == []


def test_info_validation_completed_fields():
    """
    test completed fields > true
    """

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.first_name.set("Test")
    win.surname_name.set("Test")
    win.add_1.set("Test")
    win.add_2.set("Test")
    win.email_add.set("Test")
    win.post_code.set("000 000")
    win.phone_no.set("123")

    result = win.validate_user_information_data()

    assert result == []


def test_info_validation_invalid_phone():
    """
    test invalid phone no (non-numeric) > false
    """

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.first_name.set("John")
    win.surname_name.set("Doe")
    win.add_1.set("123 Road")
    win.add_2.set("Town")
    win.email_add.set("a@b.com")
    win.phone_no.set("ABC123")  # invalid numeric input

    with patch("tkinter.messagebox.showerror") as mock_msg:
        result = win.validate_user_information_data()

    assert any("Phone Number: Is incorrect" in msg for msg in result)
    mock_msg.assert_called_once()


def test_login_validation_missing_fields():
    """
    test empty username/pass > false
    """

    # setup window class mock    
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.username.set("")
    win.password.set("")

    with patch("tkinter.messagebox.showerror"):
        result = win.validate_user_login_data()

    assert any("missing input" in msg for msg in result)


def test_login_valid():
    """
    Docstring for test_login_valid
            Test correct username/password inputs. All should pass validations            
    """    

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # new username & password meeting requirements
    win.username.set("brandnewuser")
    win.password.set("StrongPass123!")

    # valid inputs. True is passed, false is failed
    result = win.validate_user_login_data()

    assert result == []


def test_login_existing_username():
    """
    Docstring for test_login_valid
            test existing username with valid password inputs. Username already used return false       
    """    

    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # existing username within database & password meeting requirements
    win.username.set("ajones111")
    win.password.set("StrongPass123!")

    # valid inputs. True is passed, false is failed
    result = win.validate_user_login_data()

    assert result == []


def test_login_password_fails_rules():
    """
    Docstring for test_login_valid
        test existing username and invalid password. Password failures passed back to user
    """
    
    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # new username within database & invalid password
    win.username.set("ajones111")
    win.password.set("weak")

    # valid inputs. True is passed, false is failed
    result = win.validate_user_login_data()

    # check multiple input failure messages returned
    assert "Password must be at least 12 characters" in result[0]
    assert "Password must contain a capital letter" in result[1]
    assert "Password must contain a number" in result[2]


def test_postcode_validation_exist():
    """
    test postcode validation. existing code return id
    """
    
    # setup window class mock
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # valid inputs into window. None passed to ensure window data is taken
    # Returned values : True is passed, false is failed
    win.post_code.set("BS3 5RW")
    result = win.validate_postcode(None, False)

    # valid inputs. True is passed, false is failed
    assert result == "PST-007"


def test_postcode_validation_does_not_exist():
    """
    test postcode validation. non-existing code, return next id
    """

    # setup window class mock  
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    # confirm next postcode_id in sequence
    conn = uf.get_database_connection()
    sql = "SELECT 'PST-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(postcode_id, 5) AS INTEGER)) FROM postcodes), 0) + 1)"
    
    postcode_id = conn.query(sql, ())
    postcode_id = postcode_id[1][0][0]

    # valid inputs into window. None passed to ensure window data is taken
    # Returned values : True is passed, false is failed
    win.post_code.set("000 000")
    result = win.validate_postcode(None, False)

    # returned value is the next postcode_id as 000 000 doesn't exist
    assert result == postcode_id


def test_user_creation():
    """
    test user creation. 
    No record created in DB, results confirmed via result
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)
    
    win.first_name.set("Test")
    win.surname_name.set("Test")
    win.add_1.set("Test")
    win.add_2.set("Test")
    win.email_add.set("Test")
    win.post_code.set("000 000")
    win.phone_no.set("123")

    win.username.set("tester")
    win.password.set("StrongPass123!")


    result = win.validate_user_inputs(False)

    assert result == True


def test_postcode_validation_passin_code_create():
    """
    test postcode validation. Call function from other location, non-existing code, return next id
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    conn = uf.get_database_connection()
    sql = "SELECT 'PST-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(postcode_id, 5) AS INTEGER)) FROM postcodes), 0) + 1)"
    
    postcode_id = conn.query(sql, ())
    nxt_postcode_id = postcode_id[1][0][0]
    
    input_code = "000 000"
    result = win.validate_postcode(input_code, False)

    assert result == nxt_postcode_id


def test_postcode_validation_passin_code_return_existing():
    """
    test postcode validation. Call function from other location, existing code, return that id
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    conn = uf.get_database_connection()
    sql = "SELECT postcode_id FROM postcodes WHERE postcode LIKE 'CB2 1TN';"

    postcode_id = conn.query(sql, ())
    ext_postcode_id = postcode_id[1][0][0]
    
    input_code = "CB2 1TN"
    result = win.validate_postcode(input_code, False)

    assert result == ext_postcode_id