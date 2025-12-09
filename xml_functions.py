from xml.sax.saxutils import XMLGenerator
import xml.sax
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

import xml.etree.ElementTree as ET

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