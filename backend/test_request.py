import requests

url = "http://localhost:8000/api/candidates"

data = {
    "full_name": "bog",
    "telegram_username": "@Steve_Blowlobless",
    "telegram_id": "627461354",
    "results": "Passed all tests"
}

response = requests.post(url, json=data)
print("Status code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw response:", response.text)
