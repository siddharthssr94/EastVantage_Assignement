import os
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE_NAME = os.getenv('DATABASE_NAME', 'addresses.db')
DATABASE_PATH = BASE_DIR / DATABASE_NAME

try:
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, latitude REAL, longitude REAL)''')
except sqlite3.Error as e:
    print(f"An error occurred while creating the table: {e}")