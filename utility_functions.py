from icecream import ic
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import csv
import os
import database as db

def get_database_connection() -> object | bool:
    """
    Docstring for get_database_connection
                Return live database connection from settings data.
    :return: Return False if connection failure, or database connection
    :rtype: object | bool
    """
    try:
        conn = None

        # get database path/name from settings.json
        settings = get_settings_data()
        db_path = os.path.join(settings["database_settings"]["database_path"],
            settings["database_settings"]["database"])

        # Create a connection
        conn = db.Database(db_path)

        # Test created connection
        test_sql = load_sql_file("database_connection_check.sql")
        result = conn.query(test_sql, ())

        if result[1]: # sucess, return connection
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
    Docstring for load_sql_file
                Read SQL file from repsository and return as string.
    :return: If file not found, return False, else return file as full string
    :rtype: str | bool
    """
    try:
        # get path for sql file
        sql_path = os.path.join(os.path.dirname(__file__), "SQL", filename)
        
        with open(sql_path, 'r') as f: # open file * read
            sql_script = f.read()

        if sql_script: # check if file has contents
            ic(f"SQL file read successfully: {filename}")
            return sql_script # success, return str
        else:
            ic("SQL file read error") # failure return false
        
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

    # for key within json settings, return stored data
    key_str = get_settings_data()["database_settings"]["key"]
    
    # validate key & strip leading value for Fernet funciton
    if key_str.startswith("b'") or key_str.startswith('b"'):
        
        # Strip accidental b'...' wrapper
        key_str = key_str[2:-1]

    # key has been corrupted/broken
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

def validate_postcode(input_postcode: str, create:bool) -> str:
    """
    Check if postcode input exists in db
    If exist return id, if not create & return postcode_id
    create default True, if testing, pass False        
    """
    try:
        conn = None
        output = "0"

        postcode = input_postcode

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("postcode_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get next id
            if i == 0:
                postcode_id = conn.query(sql, ())
                postcode_id = postcode_id[1][0][0]

            # check if user input postcode exists
            if i == 1:
                result = conn.query(sql, (postcode,))

            # if no results create new record
            if i == 2 and not result[1] and create:
                conn.insert(sql, (postcode_id,postcode))
        
        if result[1]: 
            output = result[1][0][0]
        else:
            output = postcode_id

        # commit records (false=testing)
        # close db connection
        if create:
            conn.commit()

        conn.close()

        return output

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass
        return err
    
def get_postcode(postcode_id:str) -> tuple[bool, str | None]:
    """"
    get postcode string, from postcode_id
    
    """
    try:
        conn = None
        output = "0"

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("postcode_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get postcode from id
            if i == 3:
                postcode = conn.query(sql, (postcode_id,))

        # check for valid output
        if postcode[1][0]: 
            output = postcode[1][0][0]
        else:
            raise ValueError("Nothing found")

        # commit records (false=testing)
        conn.close(False)

        return True, output

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass

        return False, None


def validate_customer_account(user_id:str, create:bool):
    """
    Check if user_id has customer id in db, if not create
    If exist return id, if not create & return postcode_id
    create default True, if testing, pass False        
    """
    
    try:
        conn = None
        output = "0"

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("customer_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get next id
            if i == 0:
                customer_id = conn.query(sql, ())
                customer_id = customer_id[1][0][0]             

            # check if user input postcode exist
            if i == 1:
                result = conn.query(sql, (user_id,))

            # if no results create new record
            if i == 2 and not result[1] and create:
                conn.insert(sql, (customer_id,user_id))
        
        if result[1]: 
            output = result[1][0][0]
        else:
            output = customer_id

        # commit records (false=testing)
        # close db connection
        if create:
            conn.commit()

        conn.close()

        return output

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass
        return err
    
def password_requirements() -> list:
    """
    Docstring for password_requirements
    
    :return: 2 value list to pass back into msgbox
    :rtype: list
    """
    return [
    "Password Requirements", 
    " Input passwords must comply with each of the below requirements"\
        "\n1. Must contain one of the following special characters : !@#$%^&*()-+?_=,<>/ " \
        "\n2. Must be at least 12 characters" \
        "\n3. Must contain a capital letter" \
        "\n4. Must contain a number"
    ]

def xml_requirements() -> list:
    """
    Docstring for xml_requirements
    
    :return: 2 value list to pass back into msgbox
    :rtype: list
    """
    return [
    "XML file Requirements", 
        "\n1. XML file must be named after the db table being updated, i.e. access_codes, login_details ...etc" \
        "\n2. File must be over two lines, content on second line" \
        "\n3. Each element matches the db table name within a 'data' tag : e.g '<access_code>ADMIN--11</access_code>' " \
        "\n Full file example:\n" \
        '\n<?xml version="1.0" encoding="utf-8"?>' \
        '\n<root><data id="1"><access_code>ADMIN--11</access_code><description>Administrator</description></data></root>'
    ]

def staff_id_requirements() -> list:
    """
    Docstring for xml_requirements
    
    :return: 2 value list to pass back into msgbox
    :rtype: list
    """
    return [
    "Staff ID / Type Requirements", 
        "\nThe staff Type, should refect the members role, e.g. Mechanic, Front Desk ... etc" \
        "\nOnce all input and updated, a staff id number will be automatically assigned. Primary Garage can be assigned by the user within their respective 'account' tab on login"
    ]

def get_garagelist_details() -> list:
    """
    Docstring for xml_requirements
    
    :return: 2 value list to pass back into msgbox
    :rtype: list
    """
    # setup params
    text_str_create_list = []
    output_list = ["Garage Id List"]

    # get all garage details
    data = get_garage_list()

    # add into output list
    for i in data[1]:
        text_str_create_list.append(i)
    
    # combine list into str & append outmessage
    text_str_create_list = ", \n".join(text_str_create_list)
    output_list.append("\nPlease input one of the following garage ids :\n\n" + text_str_create_list)

    return output_list

def get_garage_list() -> tuple[bool, list | None]:
    """
    Docstring for get_garage_list
    
    :return: list of garage details
    :rtype: list
    :return: True for success with None, False & errorstring for failure
    :rtype: tuple[bool, str | None]
    """
    try:
        output_list = []

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("garage_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts
        for i, sql in enumerate(sql_statements):

            # get all garage_id data for dropdown
            if i == 1:
                all_garage_data = conn.query(sql, ())

                if all_garage_data:
                    output_list = []

                    # clean data intp list
                    for i in all_garage_data[1]:
                        output_list.append(i[0])

        conn.close()

        return True, output_list

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass
        return False, err



def access_code_list() -> list:
    """
    Docstring for access_codes
    
    :return: 2 value list to pass back into msgbox
    :rtype: list
    """
    # db connection & sql script get
    conn = get_database_connection()
    sql = load_sql_file("user_scripts.sql")
    sql_statements = sql.replace("\n", "").split(";")

    # enact sql scripts
    for i, sql in enumerate(sql_statements):

        # get accesscode info               
        if i == 6:
            all_accesscode_data = conn.query(sql, ())

            if all_accesscode_data:
                output_list = []

                # clean data into list
                for i in all_accesscode_data[1]:
                    output_list.append(i[0])

    output = "\n".join(output_list)

    return ["Access Codes", f"{output}"]


def validate_staff_id(user_id: str, staff_type: str, create:bool) -> str:
    """
    Docstring     Check if staff ID present for user_id in db
                If exist return id, if not create & return postcode_id
    
    :param user_id: str ... user_id for edit account
    :param staff_type: str ... string value for type of staff for edit account
    :param create: bool ... whether to update the db or allow process for testing
    :return: True for success with None, False & errorstring for failure
    :rtype: tuple[bool, str | None]
    """
    try:
        conn = None
        create_staff_id = False
        update_staff_id = False
        var_list = []
        update_var_list = []
        output = "0"

        edit_id = user_id

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("staff_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get next staff id
            if i == 0:
                staff_id = conn.query(sql, ())
                staff_id = staff_id[1][0][0]

            # check if user has staff id already
            if i == 1:
                result = conn.query(sql, (edit_id,))

                # account has staff id
                if not result[1]:
                    create_staff_id = True
                else:
                    update_staff_id = True

                    # create var list for update function
                    for i, data in enumerate(result[1][0]):
                        
                        # change the staff type var
                        if i == 2:
                            update_var_list.append(staff_type)
                        else:
                            update_var_list.append(data)
                    
                    # add edit id
                    update_var_list.append(edit_id)

            # get next mech id
            if i == 2:
                mech_id = conn.query(sql, ())
                mech_id = mech_id[1][0][0]

            # create new staff id 
            if i == 3 and create_staff_id:
                
                var_list = (
                    staff_id, 
                    edit_id,
                    staff_type,
                    mech_id
                )

                # insert into db
                conn.insert(sql, var_list)

            # update exist staff id record 
            if i == 4 and update_staff_id:
                
                # update into db
                conn.update(sql, update_var_list)

        # commit records (false=testing)
        # close db connection
        if create:
            conn.commit()

        conn.close()

        return True, None
    
    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass
        return err

def validate_primary_garage_id(user_id:str, create:bool):
    """
    Docstring     Check if garage ID present for user_id in db
             
    :param user_id: str ... user_id for login account
    :param create: bool ... whether to update the db or allow process for testing
    :return: True for success with None, False & errorstring for failure
    :rtype: tuple[bool, str | None]
    """
    
    try:
        conn = None
        output = "0"

        # db connection & sql script get
        conn = get_database_connection()
        sql = load_sql_file("garage_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get next id
            if i == 8:
                result = conn.query(sql, (user_id,))


        # commit records (false=testing)
        # close db connection
        if create:
            conn.commit()

        conn.close()

        return result[1][0][0]

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass
        return err