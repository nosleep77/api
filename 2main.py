# main.py
from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Define a root GET endpoint
@app.get("/")
async def read_root():
    # Return a welcome message
    return {"message": "Welcome to FastAPI!"}

# Define a GET endpoint with a dynamic path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    # Return the item_id and an optional query parameter 'q'
    return {"item_id": item_id, "q": q}
