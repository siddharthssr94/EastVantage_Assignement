# address_router.py
from fastapi import APIRouter, HTTPException, Depends
from models import Address
from database import get_addresses, create_address, update_address, delete_address, get_nearby_addresses
from db_utils import get_db
from typing import List

router = APIRouter()

# Create a new address
@router.post('/addresses', response_model=Address, responses={500: {"description": "Internal Server Error"}})
def create_address_route(address: Address, db=Depends(get_db)):
    """
    Creates a new address in the database.

    Args:
        address (Address): The address object to be created.
        db (sqlite3.Connection): The SQLite database connection.

    Raises:
        HTTPException: If an internal server error occurs during the database operation.

    Returns:
        Address: The created address object.
    """
    try:
        return create_address(address, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all addresses
@router.get('/addresses', response_model=List[Address], responses={500: {"description": "Internal Server Error"}})
def get_addresses_route(db=Depends(get_db)):
    """
    Retrieves all addresses from the database.

    Args:
        db (sqlite3.Connection): The SQLite database connection.

    Raises:
        HTTPException: If an internal server error occurs during the database operation.

    Returns:
        list[Address]: A list of address objects.
    """
    try:
        return get_addresses(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get addresses within a certain distance
@router.get('/addresses/nearby', response_model=List[Address], responses={500: {"description": "Internal Server Error"}})
def get_nearby_addresses_route(latitude: float, longitude: float, distance: float, db=Depends(get_db)):
    """
    Retrieves addresses within a specified distance from a given location.

    Args:
        latitude (float): The latitude of the reference location.
        longitude (float): The longitude of the reference location.
        distance (float): The maximum distance in kilometers.
        db (sqlite3.Connection): The SQLite database connection.

    Raises:
        HTTPException: If an internal server error occurs during the database operation.

    Returns:
        list[Address]: A list of address objects within the specified distance.
    """
    try:
        return get_nearby_addresses(latitude, longitude, distance, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update an address
@router.put('/addresses/{address_id}', response_model=Address, responses={404: {"description": "Address not found"}, 500: {"description": "Internal Server Error"}})
def update_address_route(address_id: int, address: Address, db=Depends(get_db)):
    """
    Updates an existing address in the database.

    Args:
        address_id (int): The ID of the address to be updated.
        address (Address): The updated address object.
        db (sqlite3.Connection): The SQLite database connection.

    Raises:
        HTTPException: If the address is not found or an internal server error occurs during the database operation.

    Returns:
        Address: The updated address object.
    """
    try:
        if not update_address(address_id, address, db):
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete an address
@router.delete('/addresses/{address_id}', responses={404: {"description": "Address not found"}, 500: {"description": "Internal Server Error"}})
def delete_address_route(address_id: int, db=Depends(get_db)):
    """
    Deletes an address from the database.

    Args:
        address_id (int): The ID of the address to be deleted.
        db (sqlite3.Connection): The SQLite database connection.

    Raises:
        HTTPException: If the address is not found or an internal server error occurs during the database operation.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        if not delete_address(address_id, db):
            raise HTTPException(status_code=404, detail="Address not found")
        return {"message": "Address deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
