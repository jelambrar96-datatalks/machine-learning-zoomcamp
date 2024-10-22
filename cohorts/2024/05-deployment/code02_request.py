import json
import requests

URL = "http://127.0.0.1:9696/predict"

client = {"job": "student", "duration": 280, "poutcome": "failure"}
res = requests.post(URL, json=client)

res_json = res.json()
print(json.dumps(res_json, indent=4))
print(res.status_code)
