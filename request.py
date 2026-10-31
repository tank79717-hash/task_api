import requests
#1
response = requests.get("http://127.0.0.1:5000/employees")
print(response.status_code)
print(response.json())
#2 