import sqlite3
import os
from PIL import Image

# Connect to DB
conn = sqlite3.connect("./database.db")
cur = conn.cursor()

# Ensure table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS stock (
    part_id TEXT PRIMARY KEY,
    image BLOB
)
""")
conn.commit()

# Open a test PNG
filepath = "C:/Users/eliot/Downloads/3769_1.jpg"
with open(filepath, "rb") as f:
    blob_data = f.read()

# Update or insert record
part_id = "TEST-001"
cur.execute("""
INSERT INTO stock(part_id, image)
VALUES(?, ?)
ON CONFLICT(part_id) DO UPDATE SET image=excluded.image
""", (part_id, blob_data))
conn.commit()
conn.close()

print("Upload successful")