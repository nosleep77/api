# main.py
from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

# Import the PostgreSQL module
from database_sql import SessionLocal, SQLItem

# Create an instance of FastAPI
app = FastAPI()

# Pydantic model for item creation (shared for both databases)
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

# Dependency to get a SQLAlchemy session for PostgreSQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create an item in PostgreSQL only
@app.post("/sql/items/", status_code=201)
def create_sql_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = SQLItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Remove SQLAlchemy internal state before returning
    sql_item_data = db_item.__dict__
    sql_item_data.pop('_sa_instance_state', None)
    return sql_item_data

# Endpoint to create an item in MongoDB only
@app.post("/nosql/items/", status_code=201)
async def create_nosql_item(item: ItemCreate = Body(...)):
    from database_nosql import item_collection, item_helper
    item_dict = item.dict()
    result = await item_collection.insert_one(item_dict)
    new_item = await item_collection.find_one({"_id": result.inserted_id})
    return item_helper(new_item)

# New endpoint to create an item in both PostgreSQL and MongoDB
@app.post("/items/", status_code=201)
async def create_item_both(item: ItemCreate, db: Session = Depends(get_db)):
    # Insert into PostgreSQL
    db_item = SQLItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Clean the SQLAlchemy object for JSON serialization
    sql_item_data = db_item.__dict__
    sql_item_data.pop('_sa_instance_state', None)

    # Insert into MongoDB
    from database_nosql import item_collection, item_helper
    item_dict = item.dict()
    result = await item_collection.insert_one(item_dict)
    mongo_item = await item_collection.find_one({"_id": result.inserted_id})
    mongo_item = item_helper(mongo_item)

    # Return a combined response
    return {"sql_item": sql_item_data, "mongo_item": mongo_item}

# Root endpoint for testing purposes
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI with PostgreSQL and MongoDB Integration!"}
