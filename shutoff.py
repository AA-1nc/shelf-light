import requests

url = 'http://10.0.0.85:5000/'
data = {
    'data': False
}

response = requests.post(url + 'toggle', json=data)
print(response.json)