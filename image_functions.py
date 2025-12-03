import utility_functions as uf
import icecream as ic
import image_functions as ifc
from PIL import Image, ImageTk
import io
import os


def upload_tk_image_to_db(img_id, filepath) -> tuple[bool, str | None]:
    """
    upload image into db as BLOB using pack_id as the key
    input img_id = part_id
    input filepath = filename to open file

    return bool, and if False errorstring
    """

    try:

        conn = None

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
        conn.close(True)
        
        return True

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass

        return False, str(err)


def get_tk_image_from_db(img_id) -> object | None:
    """
    get image from database returned as TK object ready for app display    
    img_id input is the pack_id from database 

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

        if blob[1][0][0] is None:
            return None

        # open image from blob data
        # return Tk-compatible image
        pil_img = Image.open(io.BytesIO(blob[1][0][0]))

        # Resize to fixed size
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
    

def upload_jpg_files_to_db(input_item_name: str, filepath: str) -> tuple[bool, str | None]:
    """
    pass jpg files, make transparent

    input filepath where the file is, outputpath where output is to be created, input_item_name = item_id
    """   

    try:

        from PIL import Image

        # file check
        # Check extension
        if not filepath.lower().endswith(".jpg"):
            raise ValueError("File must have .jpg extension")

        # Open the JPG image
        jpg_file = filepath
        img_id = input_item_name

        img = Image.open(jpg_file).convert("RGBA") 

        # Open the JPG
        jpg_file = "input.jpg"
    
        # Get data
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Replace white (or near-white) with transparency
            if item[0] > 240 and item[1] > 240 and item[2] > 240:  # adjust threshold
                new_data.append((255, 255, 255, 0))  # transparent
            else:
                new_data.append(item)

        # Update image data
        img.putdata(new_data)

        # Save as PNG
        img.save("./images/output.png", "PNG")

        # Convert and save as PNG
        png_file = "./images/output.png"
        img.save(png_file, "PNG")
        ifc.upload_tk_image_to_db(img_id, png_file)

        # delete temp png file
        if os.path.exists(png_file):
            os.remove(png_file)

        return True
    
    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        return False, str(err)