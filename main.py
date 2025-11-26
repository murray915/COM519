from icecream import ic
from login_window import *
from main_window import *

def postcode_validation(postcode: str, create=True) -> str:
    """
    Check if postcode input exists in db
    If exist return id, if not create & return postcode_id
    create default True, if testing, pass False        
    """
    try:

        output = "0"

        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("postcode_check.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts (3 total)
        for i, sql in enumerate(sql_statements):

            # get next id
            if i == 0:
                postcode_id = conn.query(sql, ())
                postcode_id = postcode_id[1][0][0]

            # check if user input postcode exist
            if i == 1:
                result = conn.query(sql, (postcode,))

            # if no results create new record
            if i == 2 and not result[1] and create:
                conn.insert(sql, (postcode_id,postcode))
         
        if result[1]: 
            output = result[1][0][0]
        else:
            output = postcode_id

        conn.close()

        ic(output)
        return output

    except Exception as err:
        ic(f"Unexpected error: {err}, type={type(err)}")
        conn.close()
        return err



if __name__ == "__main__":
    #Login_process = Login_Window()
    #result = Login_process.run()
    
    postcode = "L1 2SR"
    output = postcode_validation(postcode)
