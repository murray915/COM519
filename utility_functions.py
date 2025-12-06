from icecream import ic
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import csv
import os

def get_database_connection() -> object | bool:
    """
    Return live database connection from settings data.
    If invalid, return False.
    """
    import os
    import database as db

    try:
        settings = get_settings_data()

        db_path = os.path.join(
            settings["database_settings"]["database_path"],
            settings["database_settings"]["database"]
        )

        # Create a connection (DO NOT use "with" here)
        conn = db.Database(db_path)

        # Test connection
        test_sql = load_sql_file("database_connection_check.sql")
        result = conn.query(test_sql, ())

        if result[1]:
            ic("Database connection successful")
            return conn   # return open connection
        
        ic("Database connection failed")
        conn.close()
        return False

    except Exception as err:
        ic(f"Unexpected error: {err}, type={type(err)}")
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
        #ic(filename)

        # read settings file
        # return settings data as dictionary
        with open(filename, 'r') as f:
            output = json.load(f)
            #ic(output)
            return output
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False
    

def generate_encypt_key() -> str:
    """
    generate encyption key
    return key
    """

    from cryptography.fernet import Fernet
    key = Fernet.generate_key()

    return key

def get_encrypt_key() -> str:
    """
    get stored key from settings
    
    :return: stored key
    :rtype: str
    """

    key_str = get_settings_data()["database_settings"]["key"]
        
    if key_str.startswith("b'") or key_str.startswith('b"'):
        # Strip accidental b'...' wrapper
        key_str = key_str[2:-1]

    if len(key_str) != 44:
        raise ValueError("Invalid Fernet key length")
    
    return key_str


def staging_update_settings_data(data: dict, keys: list, new_value, update=True) -> dict | bool:
    """
    update settings data from input setting path:
    example: [["database_settings"]["database"]]
    full call example: "uf.staging_update_settings_data(jsonfile, ["ktinker_settings", "font_size"], 20)"
    """
    
    try:
        # get json contents
        d = data

        for key in keys[:-1]:
            d = d.setdefault(key, {})  # create nested dict if missing
        
        d[keys[-1]] = new_value
        
        if update:
            update_setting_data(data)
        
        return data
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False
    

def update_setting_data(data) -> bool:
    """
    if data != bool, update setting json file
    return bool on completion    
    """

    import json

    try:        
        # get settings file path
        filename = "settings.json"
        filename = os.path.join(os.path.dirname(__file__), "data", filename)

        # overwrite settings file
        # return settings data as dictionary    
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return True
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")  
        return False 
    

def build_matplot_objects_stocktab(data, title:str, xlabel:str, ylabel:str, columns_input: str, values_input: str):
    """
    Build and return a Matplotlib Figure.
    Inputs  : title:str, xlabel:str, ylabel:str. Self stating
            : columns_input, values_input outline the data to plot
            
    :param data: Tuple containing (header_row, data_rows)
    :return: matplotlib.figure.Figure
    """

    # create temp csv & dump data
    temp_path = "./data/temp.csv"
    with open(temp_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data[0])  # header
        writer.writerows(data[1]) # rows

    # read the data back from temp csv
    df = pd.read_csv(temp_path)

    # create the plot pivot
    pivot = df.pivot_table(
        index="year_month",
        columns=columns_input,
        values=values_input,
        aggfunc="sum"
    )

    # create plot
    fig, ax = plt.subplots(figsize=(8, 4))
    pivot.plot(ax=ax, marker="o")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.setp(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()

    # cleanup temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return fig

def is_nonnegative_whole_number(input_value) -> bool:
    """
    Docstring for is_nonnegative_whole_number
    
    :param input_value: Description
    """
    try:
        xf = float(input_value)
        return xf.is_integer() and xf >= 0
    
    except (TypeError, ValueError):
        return False