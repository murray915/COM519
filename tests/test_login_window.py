import pytest
from .test_fixtures import *
from login_window import * 
import utility_functions as uf
from unittest.mock import patch, MagicMock


def test_encypt_data():
    """
    test function to encypt/decrypt data on input
    """
    with patch('tkinter.Tk'):
        Login_process = Login_Window()
        data = Login_process.encryption("test", True)
        assert data != "test"


def test_decypt_data():
    """
    test function to encypt/decrypt data on input
    """
    with patch('tkinter.Tk'):
        Login_process = Login_Window()
        data = Login_process.encryption("test", True)
        decrypt_data = Login_process.encryption(data, False)
        assert decrypt_data == "test"