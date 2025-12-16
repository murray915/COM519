import pytest
from datetime import date, timedelta
import tkinter as tk
from unittest.mock import MagicMock, patch
from unittest.mock import Mock
from tab_book_appointments import Tab2


class MockConn:
    """Mock database connection"""
    def query(self, sql, params=None):
        # Simulate your db returning vehicle data
        # Structure: [columns, rows]
        return [
            ['customer_vehicle_id', 'REPLACE(LTRIM(RTRIM(cusveh.car_reg))," ", "")', 
             'car_make', 'car_model', 'active_flag'],
            [('CUSVEH-001', 'BK72LXF', 'Volkswagen', 'Golf', 1)]
        ]


@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def mock_controller():
    return Mock()

@pytest.fixture
def tab2(root, mock_controller):
    tab = Tab2(root, controller=mock_controller, curr_user="USR-001", style_name="TFrame")
    return tab

# def test_missing_data(tab2):
#     """
#     Docstring for test_missing_data
#             missing value
#     :param tab2: passing mock window
#     :type tab2: Tab2
#     """
#     data_list = ["", "BK72LXF"]
#     output = tab2.check_user_inputs(data_list)
#     assert any("missing input values" in msg for msg in output)

# def test_invalid_date_format(tab2):
#     """
#     Docstring for test_invalid_date_format
#             yyyy-MM-dd passed
#     :param tab2: passing mock window
#     :type tab2: Tab2
#     """
#     data_list = ["2025-12-10", "BK72LXF"]  # Wrong format
#     output = tab2.check_user_inputs(data_list)
#     assert any("Date Format should be dd/MM/yyyy" in msg for msg in output)

# def test_past_date(tab2):
#     """
#     Docstring for test_past_date
#             yesterday passed
#     :param tab2: passing mock window
#     :type tab2: Tab2
#     """    
#     data_list = ["01/01/1999", "BK72LXF"]
#     output = tab2.check_user_inputs(data_list)
#     assert any("Date is in the past" in msg for msg in output)

# def test_vehicle_not_found(tab2):
#     """
#     Docstring for test_vehicle_not_found
#             rubbish veh passed
#     :param tab2: passing mock window
#     :type tab2: Tab2
#     """    
#     data_list = ["01/01/2030", "INVALIDREG"]
#     output = tab2.check_user_inputs(data_list)
#     assert any("Vechicle Reg not found" in msg for msg in output)

# def test_all_valid(tab2):
#     """
#     Docstring for test_all_valid
#             all good
#     :param tab2: passing mock window
#     :type tab2: Tab2
#     """    
#     data_list = [date.today().strftime('%d/%m/%Y'),"BK72LXF"]
#     output = tab2.check_user_inputs(data_list)
#     # Should return empty list if no errors
#     assert output == []
