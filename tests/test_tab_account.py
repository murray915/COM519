import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch, Mock
from tab_account import Tab5

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def mock_controller():
    return Mock()

@pytest.fixture
def tab5(root, mock_controller):
    tab = Tab5(root, controller=mock_controller, curr_user="USR-001", style_name="TFrame")
    return tab

def test_encryption_and_decryption(tab5):
    original = "MyPassword123!"
    encrypted = tab5.encryption(original, True)
    decrypted = tab5.encryption(encrypted, False)

    assert original == decrypted
    assert encrypted != original


def test_check_password_valid(tab5):

    data_list = [
        ["username", "user1"],
        ["Curr_Password", "OldPass123!"],
        ["Password_1", "StrongPass123!"],
        ["Password_2", "StrongPass123!"],
    ]

    result = tab5.check_user_inputs_password(data_list)
    assert result == []


def test_check_password_missing_fields(tab5):

    data_list = [
        ["username", ""],
        ["Curr_Password", ""],
        ["Password_1", ""],
        ["Password_2", ""],
    ]

    result = tab5.check_user_inputs_password(data_list)

    assert "username: Is missing input values" in result
    assert "Curr_Password: Is missing input values" in result
    assert "Password_1: Is missing input values" in result
    assert "Password_2: Is missing input values" in result

def test_check_password_mismatch(tab5):

    data_list = [
        ["username", "user1"],
        ["Curr_Password", "OldPass123!"],
        ["Password_1", "StrongPass123!"],
        ["Password_2", "DifferentPass123!"],
    ]

    result = tab5.check_user_inputs_password(data_list)

    assert "New passwords must match" in result

