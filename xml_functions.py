from xml.sax.saxutils import XMLGenerator
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox
import utility_functions as uf
import io
import os

class XMLwriteHelper:    
    @staticmethod
    def run(columns: list, rows: list, filename: str):
        """
        Docstring for creating xml files
        
        :param columns: headers of sql tables
        :type columns: list
        :param rows: rows = data returned from sql query
        :type rows: list
        :param filename: is the output filename to be saved. Location = ./data/...
        :type filename: str
        """

        # create output memory & writer obj
        output = io.StringIO()
        writer = XMLWriter(output)
        writer.start()

        # add col/values into xml
        for row in rows:
            writer.add_row(columns, row)
        
        # create header
        writer.finish()

        # get end data
        xml_string = output.getvalue()

        # create xml outfile from xml_string value
        filename = os.path.join(os.path.dirname(__file__), "data", filename)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml_string)

class XMLWriter:
    def __init__(self, stream):
        self.gen = XMLGenerator(stream, "utf-8")
        self.row_id = 1

    def start(self): 
        # create header
        self.gen.startDocument()
        self.gen.startElement("root", {})

    def add_row(self, columns, values):
        # create header for elements
        # Add <data id="1"> ... </data>
        self.gen.startElement("data", {"id": str(self.row_id)})
        self.row_id += 1
        
        # loop through input data, matching header to values (row)
        # header of element is column from sql
        # val is the row value, "access_code" is the sql header, with value ADMIN
        # result = "<access_code>ADMIN</access_code>" for each passed column/value zipped
        for col, val in zip(columns, values):
            self.gen.startElement(col, {})
            self.gen.characters(str(val))
            self.gen.endElement(col)

        # end data section
        self.gen.endElement("data")

    def finish(self):
        # complete xml add footer
        self.gen.endElement("root")
        self.gen.endDocument()

class XMLReader:
    """
    xmlreader: returns each <data> block as a dict
        example call:
        reader = XMLReader("example/example/DB_TABLE.xml") # full filepath
        rows = reader.get_rows()

    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.tree = None
        self.root = None
        self.db_dictionary = None

    def load(self):
        """
        Load and parse the XML file.
        """
        self.tree = ET.parse(self.filepath)
        self.root = self.tree.getroot()

    def get_rows(self) -> list[dict]:
        """
        Return a list of dicts
        Each dictionary contains:
          - all attributes from <data>
          - all child nodes (tags + text)
        """
        if self.root is None:
            self.load()

        rows = []

        for data_element in self.root.findall("data"):
            row_dict = {}

            # Add attributes, e.g. id="1"
            for attr_name, attr_value in data_element.attrib.items():
                row_dict[attr_name] = attr_value

            # Add child tags and text
            for child in data_element:
                text = child.text.strip() if child.text else ""
                row_dict[child.tag] = text

            rows.append(row_dict)

        return rows    
    
    def get_db_table_details(self, table_name: str):
        """
        Docstring for get_db_table_details
        
        :param self: Description
        """
        try:
            conn = None

            # db connection & sql script get
            conn = uf.get_database_connection()
            sql = uf.load_sql_file("admin_scripts.sql")
            sql_statements = sql.replace("\n", "").split(";")
        
            # enact sql scripts
            for i, sql in enumerate(sql_statements):
                
                # get package info for dropdown
                if i == 1:
                    sql = sql.replace("replace",f'"{table_name}"')
                    data = conn.query(sql, ())

                    sql_table_data = {}

                    for i, sql_header in enumerate(data[1]):
                        
                        key = sql_header[1]
                        sql_table_data[key] = sql_header[2]

                    # update self data store
                    self.db_dictionary = sql_table_data

            # commit & close
            conn.close()

            return True

        except Exception as err:
            print(f"Unexpected error: {err}, type={type(err)}")
            if conn:
                conn.close()
            else:
                pass

            return False, str(err)

class XmlEditor(tk.Toplevel):
    def __init__(self, root, table_name, rows, on_save=None):
        super().__init__(root)
        self.window = root
        self.table_name = table_name
        self.rows = rows
        self.on_save = on_save
        self.entries = []

        self.geometry(uf.get_settings_data()["ktinker_settings"]["reg_geometry"])
        self.title(f"XML Editor")
       
        self.window_constructor()
        self.table_constructor()

    def window_constructor(self):

        # allow resizing        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # update scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # mouse wheel scrolling
        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window, width=e.width
            )
        )

        # Add buttons to window within frame
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(frame, text="Add Data", command=self.add_row)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(frame, text="Save File", command=self.save_changes)
        save_button.grid(row=2, column=4, columnspan=2, pady=10)

    def clear_previous_rows(self):
        """Clear all previous row widgets and reset entries list."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def table_constructor(self):

        # reset table
        self.clear_previous_rows()

        # build new rows
        for data_index, row_data in enumerate(self.rows):
            data_frame = ttk.LabelFrame(
                self.scrollable_frame, text=f"Data Point {data_index + 1}"
            )

            # create dataframe
            data_frame.grid(row=data_index, column=0, sticky="ew", padx=10, pady=6)

            # container for data
            row_entries = {}

            # loop through data & return values
            for field_index, (field, value) in enumerate(row_data.items()):
                ttk.Label(data_frame, text=field).grid(
                    row=field_index, column=0, sticky="w", padx=5, pady=2
                )

                entry = ttk.Entry(data_frame, width=60)
                entry.insert(0, "" if value is None else value)

                # read-only fields // don't allow edit
                if field in ("id", "image_blob"):
                    entry.config(state="disabled")

                # add to grid created entries
                entry.grid(row=field_index, column=1, padx=5, pady=2)
                row_entries[field] = entry

            # add delete to created entree
            delete_btn = ttk.Button(
                data_frame,
                text="Delete Row",
                command=lambda idx=data_index: self.delete_row(idx)
            )

            delete_btn.grid(
                row=field_index + 1, column=0, columnspan=2, pady=6
            )

            self.entries.append(row_entries)

    def add_row(self):

        new_row = {}

        existing_ids = [int(r["id"]) for r in self.rows if r.get("id")]
        next_id = str(max(existing_ids) + 1 if existing_ids else 1)
        new_row["id"] = next_id

        if self.rows:
            for key in self.rows[0]:
                if key != "id":
                    new_row[key] = None

        self.rows.append(new_row)
        self.table_constructor()

        
    def delete_row(self, index):

        if messagebox.askyesno("Confirm Delete", "Delete this row?"):
            del self.rows[index]
            
            self.table_constructor()

    def save_changes(self):

        for row_index, row_entries in enumerate(self.entries):

            # update row dict, skipping read-only fields
            self.rows[row_index].update({
                field: (entry.get() or None)
                for field, entry in row_entries.items()
                if field not in ("image_blob", "id")
            })

        if self.on_save:
            self.on_save(self.table_name, self.rows)

def database_backup(db_table_list: list) -> tuple[bool, str | None]:
    """
    Docstring for database_backup. Input db tables to pull data for
    
    :param db_table_list: list of db table names
    :type db_table_list: list
    :return: True for success, False & errorstring for failure
    :rtype: tuple[bool, str | None]
    """
    
    try:
        conn = None

        conn = uf.get_database_connection()
        sql_temp = "SELECT * FROM replace"

        for j in db_table_list:

            sql = sql_temp.replace("replace",j)
            data = conn.query(sql, ())

            columns = []
            rows = []

            for i in data[0]:
                columns.append(i)

            for i in data[1]:
                rows.append(i)

            # pass out xml files from filename list
            XMLwriteHelper.run(columns, rows, f"{j}.xml")

        # commit & close
        conn.close()

        return True

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass

        return False, str(err)

def database_updater_from_xml(filepath: str) -> tuple[bool, str | None]:
    """
    Docstring for database_updater_from_xml, requirements are xml name = db table
    
    :param filepath: str is the full filepath for the xml
    :type filepath: str
    :return: True for success, False & errorstring for failure
    :rtype: tuple[bool, str | None]
    """
    
    try:

        filename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(filename)[0]

        # read input xml from users
        reader = XMLReader(filepath)
        table_header = name_without_ext

        conn = None

        # db connection & sql script get
        conn = uf.get_database_connection()
        conn.execute("PRAGMA foreign_keys = OFF;") # remove constraits

        sql = uf.load_sql_file("admin_scripts.sql")
        sql_statements = sql.replace("\n", "").split(";")
    
        # enact sql scripts
        for i, sql in enumerate(sql_statements):
            
            # get table headers from db
            if i == 1:
                # change db table
                sql = sql.replace("replace",table_header)
                data = conn.query(sql, ())
                
                # collect data
                header = []

                for i in data[1]:
                    header.append(i[1])

                # convert to str
                header_str = ','.join(header) 

            # insert into respective db
            if i == 2:
                # update sql for respective db table
                sql = sql.replace("replace0",name_without_ext)

                # update values with respective number of ? (based on db table headers)
                placeholders_values = ", ".join("?" for _ in header)
                sql_template = sql.replace("replace1",header_str).replace("replace2",placeholders_values) # template sql for insert loop 

                # read input xml data
                rows = reader.get_rows()

                # loop to get input data from xml
                for row in rows:
                    row_data = []

                    # get only values per key
                    for idx, (key, value) in enumerate(row.items()):                
                        if idx >= 1:
                            row_data.append(value)
                
                    # update sql, for each looped values
                    conn.insert(sql_template, row_data)
                    
        # commit & close
        conn.close(True)

        return True, None

    except Exception as err:
        print(f"Unexpected error: {err}, type={type(err)}")
        if conn:
            conn.close()
        else:
            pass

        return False, str(err)

def load_xml_as_rows(xml_path):

    # read input xml path
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # empty list
    rows = []
    
    # loop through tree, for data tag
    for data_elem in root.findall("data"):

        # id denotes entity start
        row = {"id": data_elem.get("id")}

        # get branch data
        for child in data_elem:
            row[child.tag] = child.text

        # append end list    
        rows.append(row)

    return rows
