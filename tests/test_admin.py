import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tab_admin import Tab7
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
def tab7(root, mock_controller):
    tab = Tab7(root, controller=mock_controller, curr_user="USR-001", style_name="TFrame")
    return tab


def test_check_user_inputs_password_valid(tab7):
    """
    Password + accesscode + activeflag are valid
    """
    data = [
        "ValidPassword123!",    # meets all rules
        "CUS_USR",              # in access list
        "Active"                # valid
    ]

    # fixture for window
    result = tab7.check_user_inputs_password(data)
    assert result == []

def test_check_user_inputs_password_invalid(tab7):
    """Test missing capitals, numbers, invalid access code, etc."""
    data = [
        "short",       # 5 chars = invalid
        "UNKNOWN",     # not in access_code_list
        "maybe"        # invalid activeflag
    ]

    # fixture for window
    result = tab7.check_user_inputs_password(data)

    assert "Password must be at least 12 characters" in result
    assert "Password must contain a capital letter" in result
    assert "Password must contain a number" in result
    assert "Password must contain a special character" in result
    assert "Access code input is not supported." in result
    assert "Activeflag needs to be Active or Inactive" in result


def test_check_user_inputs_allmissing_invalid(tab7):
    """Test missing values passed, numbers, invalid access code, etc."""
    data = [
        "",
        "",
        ""
    ]

    # fixture for window
    result = tab7.check_user_inputs_password(data)

    assert "Activeflag needs to be Active or Inactive" in result
