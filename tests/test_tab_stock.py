import pytest
from .test_fixtures import *
from tab_stock import *
from unittest.mock import patch, MagicMock, Mock

import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"

@pytest.fixture
def mock_controller():
    return Mock()

def test_create_new_item_missing_data(mock_controller):
    """
    test empty fields > false
    """
    curr_user = "USR-001"
    parent = None
    win = Tab3.__new__(Tab3)

    Tab3.__init__(win, parent, mock_controller, curr_user, "TabFrame.TFrame")
    

    win.new_item_name.set("")
    win.new_item_des.set("")
    win.new_item_comm_group.set("")

    result = win.create_new_item(False)

    if type(result) == tuple:
        assert result[0] is False
    else:
        assert result is False


def test_create_new_item_correct_data(mock_controller):
    """
    test completed fields > true
    """
    curr_user = "USR-001"
    parent = None
    win = Tab3.__new__(Tab3)

    Tab3.__init__(win, parent, mock_controller, curr_user, "TabFrame.TFrame")    

    win.new_item_name.set("TEST")
    win.new_item_des.set("sasfa  asfasvas")
    win.new_item_comm_group.set("Commonnnnn")

    result = win.create_new_item(False)

    if type(result) == tuple:
        assert result[0] is True
    else:
        assert result is True