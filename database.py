# database.py
from db_utils import get_db
from models import Address
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on a sphere given their longitudes and latitudes.

    Args:
        lat1 (float): Latitude of the first point in degrees.
        lon1 (float): Longitude of the first point in degrees.
        lat2 (float): Latitude of the second point in degrees.
        lon2 (float): Longitude of the second point in degrees.

    Returns:
        float: The distance between the two points in kilometers.
    """
    # Convert to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def create_address(address: Address, db):
    """
    Create a new address in the database.

    Args:
        address (Address): The address object to be created.
        db (sqlite3.Connection): A database connection object.

    Returns:
        Address: The created address object.
    """
    try:
        name = address.name
        latitude = address.latitude
        longitude = address.longitude
        db.execute("INSERT INTO addresses (name, latitude, longitude) VALUES (?, ?, ?)", (name, latitude, longitude))
        db.commit()
        return address
    except Exception as e:
        print("Error creating address:", e)
        return None

def get_addresses(db):
    """
    Retrieve all addresses from the database.

    Args:
        db (sqlite3.Connection): A database connection object.

    Returns:
        list[Address]: A list of address objects.
    """
    try:
        cursor = db.execute("SELECT name, latitude, longitude FROM addresses")
        addresses = [Address(name=row[0], latitude=row[1], longitude=row[2]) for row in cursor.fetchall()]
        return addresses
    except Exception as e:
        print("Error getting addresses:", e)
        return []

def get_nearby_addresses(latitude: float, longitude: float, distance: float, db):
    """
    Retrieve addresses within a specified distance from a given location.

    Args:
        latitude (float): The latitude of the reference location.
        longitude (float): The longitude of the reference location.
        distance (float): The maximum distance in kilometers.
        db (sqlite3.Connection): A database connection object.

    Returns:
        list[Address]: A list of address objects within the specified distance.
    """
    try:
        addresses = []
        cursor = db.execute("SELECT name, latitude, longitude FROM addresses")
        for row in cursor.fetchall():
            addr = Address(name=row[0], latitude=row[1], longitude=row[2])
            dist = haversine(latitude, longitude, addr.latitude, addr.longitude)
            if dist <= distance:
                addresses.append(addr)
        return addresses
    except Exception as e:
        print("Error getting nearby addresses:", e)
        return []

def update_address(address_id: int, address: Address, db):
    """
    Update an existing address in the database.

    Args:
        address_id (int): The ID of the address to be updated.
        address (Address): The updated address object.
        db (sqlite3.Connection): A database connection object.

    Returns:
        bool: True if the address was updated successfully, False otherwise.
    """
    try:
        cursor = db.execute("SELECT * FROM addresses WHERE id=?", (address_id,))
        existing_address = cursor.fetchone()
        if existing_address is None:
            return False
        db.execute("UPDATE addresses SET name=?, latitude=?, longitude=? WHERE id=?",
                   (address.name, address.latitude, address.longitude, address_id))
        db.commit()
        return True
    except Exception as e:
        print("Error updating address:", e)
        return False

def delete_address(address_id: int, db):
    """
    Delete an address from the database.

    Args:
        address_id (int): The ID of the address to be deleted.
        db (sqlite3.Connection): A database connection object.

    Returns:
        bool: True if the address was deleted successfully, False otherwise.
    """
    try:
        cursor = db.execute("SELECT * FROM addresses WHERE id=?", (address_id,))
        existing_address = cursor.fetchone()
        if existing_address is None:
            return False
        db.execute("DELETE FROM addresses WHERE id=?", (address_id,))
        db.commit()
        return True
    except Exception as e:
        print("Error deleting address:", e)
        return False