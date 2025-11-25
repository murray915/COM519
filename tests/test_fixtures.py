import pytest
import tkinter as tk

@pytest.fixture
def settings_json():    
    return {
        "main_settings": {
            "theme": "dark",
            "font_size": 12,
            "language": "en" 
        },   

        "database_settings": {
            "database": "database.db",
            "database_path": "./data/",
            "key": "b'IBlCrg4jbPD7WSy0NjFIucP2pMS-_32xBpBCDw1S3kk='"
        },

        "programming_settings": {
            "icecream_enabled": "true"  
        },

        "ktinker_settings": {
            "login_geometry": "300x100",
            "reg_geometry": "650x450",
            "app_geometry": "1200x600"
        }
    }


@pytest.fixture(autouse=True)
def mock_stringvar(monkeypatch):
    class FakeVar:
        def __init__(self, value=""):
            self._v = value
        def get(self):
            return self._v
        def set(self, v):
            self._v = v


@pytest.fixture(autouse=True)
def mock_messagebox(monkeypatch):
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)