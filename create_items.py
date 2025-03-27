#!/usr/bin/env python3
import requests

# URL for the FastAPI endpoint that creates an item in PostgreSQL
url = "http://127.0.0.1:8000/sql/items/"

# Loop to create 100 items
for i in range(100):
    # Construct the payload with unique data for each item
    payload = {
        "name": f"Item {i + 1}",
        "description": f"Description for item {i + 1}",
        "price": round(10.0 + i * 0.5, 2),  # Example price calculation
        "in_stock": True
    }
    
    # Send a POST request with JSON payload
    response = requests.post(url, json=payload)
    
    # Check response status and print the result
    if response.status_code == 201:
        print(f"Created Item {i + 1}")
    else:
        print(f"Failed to create Item {i + 1}: {response.text}")
