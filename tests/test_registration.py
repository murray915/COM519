import pytest
from .test_fixtures import *
from registration_window import *

import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"


def test_info_validation_missing_fields(monkeypatch):
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
    win.phone_no.set("")

    result = win.validate_user_information_data()

    assert result is False


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
    win.phone_no.set("123")

    result = win.validate_user_information_data()

    assert result is True