from flask import Flask, jsonify, request, render_template
import requests
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("mongodb+srv://AashK:ProgBDAT@cluster0.tirts.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.test  
records = db.cadExchange

# number of days for which data is available
number_days = len(list(records.find()))

# get dates
dates = []
for i in range(number_days):
    get_datetime = pd.to_datetime(list(records.find())[i]['time_last_update_utc'])
    dates += [get_datetime.date()]

# get rates
rates = []
for i in range(number_days):
    rates += [list(records.find())[i]['conversion_rates']]
    
# create dataframe
db_data = pd.DataFrame(rates, index = dates)
second_last_index = db_data.shape[0]-2
last_index = db_data.shape[0]-1

# --------------------- Main Currencies  ---------------------------------------------
def main_Cs(x):
    t = {"Currency": "Amount in CAD"}
    for i in ['CAD','USD','EUR','CNY','GBP']:
        t[i]=round(1/x.iloc[last_index].to_dict()[i],2)
    return t

main_currencies = main_Cs(db_data)

# ----------------------- Most Valuable Currencies ------------------------------------

def return_valuable(x):
    
    today_series = pd.Series(x.iloc[last_index])
    sorted_value = (1/(today_series.sort_values(axis=0)))
    
    sorted_valuable = sorted_value[:5].to_dict()
    a = {'Currency': 'Amount in CAD'}
    for i in sorted_valuable:
        a[i] = sorted_valuable[i]
    return a
        
valuable = return_valuable(db_data)

# ----------------------- Least Valuable Currencies ------------------------------------

def return_least(x):
    
    today_series = pd.Series(x.iloc[last_index])
    sorted_value = (1/(today_series.sort_values(axis=0)))
    
    sorted_valuable = sorted_value[-5:].to_dict()
    a = {'Currency': 'Amount in CAD'}
    for i in sorted_valuable:
        a[i] = sorted_valuable[i]
    return a
        
least = return_least(db_data)

# ----------------------- Back to Flask -----------------------------------------------

@app.route('/')
def currencies():
    # data = {'Task': 'Hours per Day', 'Work': 11, 'Eat': 2, 'Commute': 2, 'Watching TV': 2, 'Sleeping': 7}
    # return render_template('pie-chart.html', data=top10(db_data))
    return render_template('currencies.html', data = main_currencies, data2 = volatility, data3 = valuable, data4 = least)

if __name__=="__main__":
    app.run()