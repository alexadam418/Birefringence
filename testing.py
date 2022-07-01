import requests
import time
import json


api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
command = 'G1 X100 Z65.11 F200'
api_url = 'http://192.168.1.2/api/printer?exclude=temperature,sd'

headers = {'Content-Type': 'application/json',
           'x-Api-Key': api_key
           }


response = requests.get(api_url, headers=headers)  # either json=data or data=data
print(response.json())

