import json
import requests

URL = "http://127.0.0.1:9696/predict"

client = {"job": "management", "duration": 400, "poutcome": "success"}
res = requests.post(URL, json=client)

res_json = res.json()
print(json.dumps(res_json, indent=4))
print(res.status_code)
