import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import io
import os
import tempfile

import image_functions as ifc  # replace with your module name

def create_temp_image(format="PNG") -> str:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{format.lower()}")
    img = Image.new("RGB", (10, 10), color="white")
    img.save(tmp_file.name, format=format)
    tmp_file.close()
    return tmp_file.name

@patch("image_functions.uf.get_database_connection")
@patch("image_functions.uf.load_sql_file")
def test_get_tk_image_from_db_no_image(mock_load_sql, mock_db_conn):
    mock_conn = MagicMock()
    mock_conn.query.return_value = (None, [[None]])
    mock_db_conn.return_value = mock_conn
    mock_load_sql.return_value = "SQL1;SQL2;"

    result = ifc.get_tk_image_from_db("IMG001")
    assert result is None
    mock_conn.close.assert_called_once_with(True)