import pytest
from .test_fixtures import *
from utility_functions import * 

def test_database_connection_pass():
        """ 
        confirm that database connection works & passed back in function
        """

        import database as db

        settings = get_settings_data()

        db_path = os.path.join(
            settings["database_settings"]["database_path"],
            settings["database_settings"]["database"]
        )

        # Create a connection
        conn = db.Database(db_path)

        # Test connection
        test_sql = load_sql_file("database_connection_check.sql")
        result = conn.query(test_sql, ())

        conn.close()

        assert result != None


def test_get_sql_scripts():
    """
    get and read sql scripts from repository
    """
    import os

    filename = "database_connection_check.sql"
    sql_path = os.path.join(os.path.dirname(__file__).replace("\\tests",""), "SQL", filename)

    with open(sql_path, 'r') as f:
        sql_script = f.read()
   
    assert sql_script != None


def test_generate_key():
    """
    generate encyption new key from function
    return key
    """
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()

    assert key != None


def test_get_settings_key():
    """
    retrieve encyption key from settings.json
    return key
    """
    import json
    filename = ".\\data\\settings.json"

    # read settings file
    # return settings data as dictionary
    with open(filename, 'r') as f:
        output = json.load(f)
    
    assert output["database_settings"]["key"] != None


def test_update_database_key(settings_json):
    new_key = "b'NEW_FAKE_KEY_1234567890=='"    
    # Call the update function
    staging_update_settings_data(settings_json, ["database_settings", "key"], new_key,False)
    
    # Assert the value was updated
    assert settings_json["database_settings"]["key"] == new_key


def test_update_nested_nonexistent_key(settings_json):
    # Update a nested key that does not exist yet
    staging_update_settings_data(settings_json, ["ktinker_settings", "new_setting"], "value123",False)

    # Assert the value was updated    
    assert settings_json["ktinker_settings"]["new_setting"] == "value123"


def test_update_top_level_key(settings_json):
    # Update a nested key that does not exist yet
    staging_update_settings_data(settings_json, ["main_settings", "theme"], "light",False)
    
    # Assert the value was updated   
    assert settings_json["main_settings"]["theme"] == "light"