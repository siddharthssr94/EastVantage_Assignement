#create_sample_db.py
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('addresses.db')
c = conn.cursor()

# Create the addresses table
c.execute('''CREATE TABLE IF NOT EXISTS addresses
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, latitude REAL, longitude REAL)''')

# Insert some sample data
addresses = [
    ('Address 1', 37.7749, -122.4194),
    ('Address 2', 51.5072, -0.1275),
    ('Address 3', -33.8588, 151.2153),
    ('Address 4', 35.6895, 139.6917),
    ('Address 5', 41.9028, 12.4964),
]

c.executemany("INSERT INTO addresses (name, latitude, longitude) VALUES (?, ?, ?)", addresses)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample database 'addresses.db' created successfully.")