import requests

url = "http://127.0.0.1:5000/hello"

response = requests.get(url)

print("Status:", response.status_code)
print("Resposta:", response.json())