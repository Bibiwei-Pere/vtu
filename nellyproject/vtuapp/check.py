import json,requests
from requests.auth import HTTPBasicAuth
import requests

url = "https://smeplug.ng/api/v1/data/plans"

payload = {}
headers = {
  'Authorization': 'Bearer f756602f3b8953f2de86d83769742979e1d780f063be86b711e68bc8518245f5'
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))