import pandas as pd
import numpy as np
import requests
import time
import os

# read csv to dataframe
df = pd.read_csv('data.csv', header=0, names=["Time", "Balance"])

# request headers
headers_dict = {
    "Cookie": "CFID=39674701; CFTOKEN=85793193; _opensaml_req_ss%3Amem%3A78116d36e20c026c8193124127deb7c03f5c617d533a3bebf9f5d07607b8b72a=_755701b6cdb6fbbd1447da9b15f89fec; _opensaml_req_ss%3Amem%3Ab53c175403228b2baff914c51f410b92d126fd8074f001691361edb9670c6a07=_a87f5d874fa1fba142ca44922ef62b40; JSESSIONID=3D537D0150ECB50990C329AF6445BC23.app; \
    _shibsession_64656661756c7468747470733a2f2f7777772e61627365636f6d2e7073752e6564752f73686962626f6c657468=_9d109b0c13deb6be43e879728edcd907; JSESSIONID=B5253D7E9A6B58EBA9E458B9A7442DEC.app",
}

download_req = requests.get(
        "https://www.absecom.psu.edu/eLIVING_STUDENT/student-pages/buy-meal-plan/buy-meal-plan-win.cfm",
        headers=headers_dict,
)

balance = download_req.text.split("<td class=\"data-label bt-0\">Account Balance</td>",1)[1]
balance = balance.split("<td colspan=\"3\" class=\"bt-0\">$", 1)[1]
balance = balance.split("</td>", 1)[0]

if df.iloc[len(df)-1]['Balance'] != np.float64(balance): 
    df_new_entry = pd.DataFrame({'Time':[int(time.time())], 'Balance':[balance]})
    df = pd.concat([df,df_new_entry], ignore_index=True)

print(df)

df.to_csv("data.csv")