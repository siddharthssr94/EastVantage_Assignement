import sqlite3
from fastapi import FastAPI
from address_router import router
from db_utils import create_table, get_db

app = FastAPI()
app.include_router(router)

try:
    with get_db() as db:
        create_table(db)
except sqlite3.Error as e:
    print(f"An error occurred while creating the table: {e}")

@app.get("/")
def root():
    """ Root endpoint of the API.
    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Address Book API"}

# Run the app with uvicorn
# uvicorn main:app --reload