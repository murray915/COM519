import utility_functions as uf
import icecream as ic
from PIL import Image, ImageTk
import io


def upload_tk_image_to_db(img_id, filepath) -> tuple[bool, str | None]:
    """
    upload image into db as BLOB using pack_id as the key
    input img_id = pack_id
    input filepath = filename to open file

    return bool, and if False errorstring
    """

    try:

        # file check
        # Check extension
        if not filepath.lower().endswith(".png"):
            raise ValueError("File must have .png extension")

        # Read file
        with open(filepath, "rb") as f:
            blob_data = f.read()

        # Validate PNG signature
        if blob_data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("File is not a valid PNG image")

        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("database_image_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts
        for i, sql in enumerate(sql_statements):

            # insert blob data into db
            if i == 1:
                conn.update(sql, (blob_data,img_id))


        # commit & close connections
        conn.commit()
        conn.close()
        
        return True

    except Exception as err:
        ic(f"Unexpected error: {err}, type={type(err)}")
        conn.close()
        return False, str(err)


def get_tk_image_from_db(img_id) -> tuple[object | None, bool, str | None]:
    """
    get image from database returned as TK object ready for app display    
    img_id input is the pack_id from database 

    return object|None, false/true and errorstring if false(err occured)
    """   

    try:
        # db connection & sql script get
        conn = uf.get_database_connection()
        sql = uf.load_sql_file("database_image_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")

        # enact sql scripts
        for i, sql in enumerate(sql_statements):

            # get blob data from id
            if i == 0:
                blob = conn.query(sql, (img_id,))

        # commit & close connections
        conn.commit()
        conn.close()

        # open image from blob data
        # return Tk-compatible image
        pil_img = Image.open(io.BytesIO(blob))
        return ImageTk.PhotoImage(pil_img)

    except Exception as err:
        ic(f"Unexpected error: {err}, type={type(err)}")
        conn.close()
        return False, str(err)