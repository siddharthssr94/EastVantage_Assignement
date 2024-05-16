import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / 'addresses.db'

def get_db():
    """ Returns the SQLite database connection.
    Returns:
        sqlite3.Connection: The SQLite database connection.
    """
    try:
        conn = sqlite3.connect(str(DATABASE_PATH), detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row  # This line will allow you to access rows using string keys
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        raise

def create_table(db):
    """ Creates the 'addresses' table in the database if it doesn't exist.
    Args:
        db (sqlite3.Connection): The SQLite database connection.
    """
    try:
        db.execute('''CREATE TABLE IF NOT EXISTS addresses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, latitude REAL, longitude REAL)''')
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
        raise