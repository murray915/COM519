import pytest
from .test_fixtures import *
from registration_window import *
from unittest.mock import patch, MagicMock

import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"


def test_info_validation_all_missing_fields(monkeypatch):
    """
    test empty fields > true
    """

    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.first_name.set("")
    win.surname_name.set("")
    win.add_1.set("")
    win.add_2.set("")
    win.email_add.set("")
    win.post_code.set("")
    win.phone_no.set("")

    result = win.validate_user_information_data()

    assert result is False


def test_info_validation_some_missing_fields(monkeypatch):
    """
    test single empty field > true
    """

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

    assert result is False


def test_info_validation_incorrectpass_fields(monkeypatch):
    """
    test valid phone no passed as non-str > true
    """

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

    assert result is True


def test_info_validation_completed_fields(monkeypatch):
    """
    test completed fields > true
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

    result = win.validate_user_information_data()

    assert result is True


def test_info_validation_invalid_phone():
    """
    test invalid phone no (non-numeric) > false
    """

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

    assert result is False
    mock_msg.assert_called_once()


def test_login_validation_missing_fields():
    """
    test empty username/pass > false
    """
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.username.set("")
    win.password.set("")

    with patch("tkinter.messagebox.showerror"):
        result = win.validate_user_login_data()

    assert result is False


def test_login_valid():
    """
    test correct username/pass > true
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.username.set("brandnewuser")
    win.password.set("StrongPass123!")

    result = win.validate_user_login_data()

    assert result is True


def test_login_existing_username():
    """
    test empty username/pass. Username already used > false
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.username.set("ajones1")
    win.password.set("StrongPass123!")

    result = win.validate_user_login_data()

    assert result is False


def test_login_password_fails_rules():
    """
    test empty username/pass. Username already used > false
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.username.set("brandnewuser")
    win.password.set("weak")

    result = win.validate_user_login_data()

    assert result is False


def test_postcode_validation_exist():
    """
    test postcode validation. existing code return id
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    win.post_code.set("BS3 5RW")
    result = win.validate_postcode(False)

    assert result == "PST-007"


def test_postcode_validation_does_not_exist():
    """
    test postcode validation. non-existing code, return next id
    """
        
    win = Reg_Window.__new__(Reg_Window)
    Reg_Window.__init__(win, parent=None)

    conn = uf.get_database_connection()
    sql = "SELECT 'PST-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(postcode_id, 5) AS INTEGER)) FROM postcodes), 0) + 1)"
    
    postcode_id = conn.query(sql, ())
    postcode_id = postcode_id[1][0][0]
    
    win.post_code.set("000 000")
    result = win.validate_postcode(False)

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