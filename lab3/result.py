import requests

# URL сервера
url = "http://127.0.0.1:5000/number/"

#GET
get_response = requests.get(url, params={'param': 5})
print("GET response:", get_response.json())

#POST
post_response = requests.post(url, json={'jsonParam': 10})
print("POST response:", post_response.json())

#DELETE
delete_response = requests.delete(url)
print("DELETE response:", delete_response.json())