import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tab_packages import Tab4 
from unittest.mock import Mock

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def mock_controller():
    return Mock()

@pytest.fixture
def tab4(root, mock_controller):
    tab = Tab4(root, controller=mock_controller, curr_user="USR-001", style_name="TFrame")
    return tab

def test_validate_itm_list_valid(tab4):
    """ check input list within checker returns false """
    assert tab4.validate_itm_list("ITM-001,ITM-002,ITM-123") is True
    assert tab4.validate_itm_list("ITM-999") is True
    assert tab4.validate_itm_list("N/A") is True

def test_validate_itm_list_invalid(tab4):
    """ check input list within checker returns true """
    assert tab4.validate_itm_list("ITM-01") is False
    assert tab4.validate_itm_list("ITM-1234") is False
    assert tab4.validate_itm_list("ITM-001,ABC-123") is False

@patch("tkinter.messagebox.showerror")
def test_check_user_inputs_valid(mock_msgbox, tab4):
    """ full run of user information checker. All ok """
    variable_list = ["Name", "Desc", "ITM-001,ITM-002", 1]
    result, err = tab4.check_user_inputs(variable_list, active_flag=1, items_consumed="ITM-001,ITM-002")
    assert result is True
    assert err is None
    mock_msgbox.assert_not_called()

@patch("tkinter.messagebox.showerror")
def test_check_user_inputs_missing_variable(mock_msgbox, tab4):
    """ full run of user information checker. Missing var """
    variable_list = ["Name", "", "ITM-001", 1]
    result, err = tab4.check_user_inputs(variable_list, active_flag=1, items_consumed="ITM-001")
    assert result is False
    assert "Missing data" in err
    mock_msgbox.assert_called_once()

@patch("tkinter.messagebox.showerror")
def test_check_user_inputs_invalid_active_flag(mock_msgbox, tab4):
    """ full run of user information checker. Active fllag incorrect (bool 1/0 expected) """
    variable_list = ["Name", "Desc", "ITM-001", 2]
    result, err = tab4.check_user_inputs(variable_list, active_flag=2, items_consumed="ITM-001")
    assert result is False
    mock_msgbox.assert_called_once()

@patch("tkinter.messagebox.showerror")
def test_check_user_inputs_invalid_items_consumed(mock_msgbox, tab4):
    """ full run of user information checker. incorrect list input """
    variable_list = ["Name", "Desc", 123, 1]
    result, err = tab4.check_user_inputs(variable_list, active_flag=1, items_consumed=123)
    assert result is False
    mock_msgbox.assert_called_once()