from icecream import ic
import os

def get_database_connection() -> object | bool:
    """ 
    Return database connection from settings data
    If settings data is invalid, return False    
    """

    import database as db

    try:
        
        # Get database settings from settings.json 
        database_details = get_settings_data() # get settings data
        database_settings = os.path.join(
            database_details["database_settings"]["database_path"],
            database_details["database_settings"]["database"]
            )
        
        # Debug
        ic(database_settings)

        # check database connections from settings
        with db.Database(database_settings) as db:
            database = db
            test_sql = load_sql_file("database_connection_check.sql")
            result = db.query(test_sql, ())

        # return database connection if successful
        # else return False
        if result[1]:
            ic("Database connection successful")
            return db
        else:
            ic("Database connection failed")
    
        return False
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False


def load_sql_file(filename) -> str | False: 
    """
    Read SQL file from repsository and return as string
    If file not found, return False
    """

    try:
        sql_path = os.path.join(os.path.dirname(__file__), "SQL", filename)
        
        with open(sql_path, 'r') as f:
            sql_script = f.read()

        if sql_script:
            ic(f"SQL file read successfully: {filename}")
            return sql_script
        else:
            ic("SQL file read error")
        
        return False  
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False
    

def get_settings_data() -> dict | bool:
    """ 
    Return settings data from settings.json
    If settings data is invalid, return False    
    """

    import json

    try:        
        # get settings file path
        filename = "settings.json"
        filename = os.path.join(os.path.dirname(__file__), "data", filename)
        ic(filename)

        # read settings file
        # return settings data as dictionary
        with open(filename, 'r') as f:
            output = json.load(f)
            ic(output)
            return output
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False