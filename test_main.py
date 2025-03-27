# test_main.py
from fastapi.testclient import TestClient  # Import TestClient to simulate API calls
from main import app                     # Import your FastAPI app

# Create an instance of TestClient using your FastAPI app
client = TestClient(app)

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    # Check that the response status is 200 (OK)
    assert response.status_code == 200
    # Check that the response JSON matches the expected output
    assert response.json() == {"message": "Welcome to FastAPI!"}

# Test creating an item and retrieving it
def test_create_item_and_read_item():
    # Define sample item data
    item_data = {
        "name": "Test Item",
        "description": "Testing item creation",
        "price": 9.99,
        "in_stock": True
    }
    # POST request to create the item
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    json_response = response.json()
    # Verify that the response contains an 'item_id' and the 'item' data
    assert "item_id" in json_response
    assert "item" in json_response

    # Use the returned item_id to fetch the created item
    item_id = json_response["item_id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    # The retrieved item should match the original data
    assert response.json() == item_data

# Test retrieving all items
def test_read_all_items():
    # Retrieve all items
    response = client.get("/items/")
    assert response.status_code == 200
    json_response = response.json()
    # Ensure that the response is a dictionary with item IDs as keys
    assert isinstance(json_response, dict)
