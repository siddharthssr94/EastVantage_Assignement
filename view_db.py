# view_db.py
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('addresses.db')
c = conn.cursor()

# Query the addresses table
c.execute("SELECT * FROM addresses")
addresses = c.fetchall()

# Print the table headers
print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Name", "Latitude", "Longitude"))
print("-" * 50)

# Print each row
for row in addresses:
    id, name, latitude, longitude = row
    print("{:<5} {:<20} {:<10} {:<10}".format(id, name, latitude, longitude))

# Close the connection
conn.close()