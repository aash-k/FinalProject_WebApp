import requests
import time
from pymongo import MongoClient



client = MongoClient("mongodb+srv://AashK:ProgBDAT@cluster0.tirts.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test
records = db.cadExchange

while True:
    r = requests.get('https://v6.exchangerate-api.com/v6/dfa4e76545576b583c390efd/latest/CAD')
    if r.status_code==200:
        data=r.json()
        records.insert_one(data)
        time.sleep(86400)
    else:
        print('error')
        exit()