# database_nosql.py
import motor.motor_asyncio

# Connection details for your locally installed MongoDB instance
MONGO_DETAILS = "mongodb://localhost:27017"

# Create an asynchronous MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Define the database and collection
database = client.api_database
item_collection = database.get_collection("items_collection")

# Helper function to format MongoDB documents into a Python dictionary
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "in_stock": item["in_stock"]
    }
