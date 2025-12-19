import os
import io
from PIL import Image, ImageTk
from database import Database
import utility_functions as uf

def upload_image_to_db(part_id: str, filepath: str) -> tuple[bool, str | None]:
    """
    Upload a PNG or JPG image into the stock table as a BLOB.
    If JPG, it will be converted to PNG with white made transparent.

    :param part_id: the part_id of the stock item
    :param filepath: path to the PNG or JPG image
    :return: (success: bool, error_message: str | None)
    """
    try:
        if not os.path.exists(filepath):
            return False, "File does not exist"

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg"):
            return False, "File must be PNG or JPG"

        # Convert JPG → PNG if needed
        if ext in (".jpg", ".jpeg"):
            img = Image.open(filepath).convert("RGBA")

            # Make white (or near white) transparent
            new_data = [
                (255, 255, 255, 0) if r > 240 and g > 240 and b > 240 else (r, g, b, a)
                for r, g, b, a in img.getdata()
            ]
            img.putdata(new_data)

            tmp_png = "./images/tmp_upload.png"
            os.makedirs(os.path.dirname(tmp_png), exist_ok=True)
            img.save(tmp_png, "PNG")
            upload_path = tmp_png
        else:
            upload_path = filepath

        # Read image bytes
        with open(upload_path, "rb") as f:
            blob_data = f.read()

        # Store in DB using your Database class
        with Database("./data/database.db") as db_conn:
            sql = "UPDATE stock SET image = ? WHERE part_id = ?;"
            db_conn.update(sql, (blob_data, part_id))
            db_conn.commit()

        # Clean up temporary PNG if created
        if ext in (".jpg", ".jpeg") and os.path.exists(tmp_png):
            os.remove(tmp_png)

        return True, None

    except Exception as e:
        return False, str(e)


def get_tk_image_from_db(img_id) -> object | None:
    """
    get image from database returned as TK object ready for app display    
    img_id input is the part_id from database 

    return object|None, false/true and errorstring if false(err occured)
    """   

    try:
        conn = None

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
        conn.close(True)

        # check if no data is found. If not return None
        if blob[1][0][0] is None:
            return None

        # open image from blob data
        # return Tk-compatible image
        pil_img = Image.open(io.BytesIO(blob[1][0][0]))

        # Resize to fixed possible over-sized images uploaded
        pil_resized = pil_img.resize((150,150), Image.LANCZOS)

        # Convert PIL to Tk image
        tk_img = ImageTk.PhotoImage(pil_resized)

        return tk_img
    

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass

        return False, str(err)
