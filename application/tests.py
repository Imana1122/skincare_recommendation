import requests

BASE_URL = "http://127.0.0.1:5000/"

# Dummy data for testing
dummy_data = {
    "tone": 4,
    "type": "dry",
    "features": {
        "normal": 1,
        "dry": 1,
        "oily": 1,
        "combination": 0,
        "acne": 1,
        "sensitive": 0,
        "fine lines": 0,
        "wrinkles": 0,
        "redness": 1,
        "dull": 0,
        "pore": 0,
        "pigmentation": 0,
        "blackheads": 1,
        "whiteheads": 0,
        "blemishes": 1,
        "dark circles": 0,
        "eye bags": 1,
        "dark spots": 0,
    },
}

# Make a PUT request to the /recommend endpoint
response = requests.put(BASE_URL + "recommend", json=dummy_data)

# Print the status code and response content
print("Status Code:", response.status_code)
print("Response Content:", response.json())


