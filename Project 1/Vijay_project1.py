#Vibha Vijay vgv9sn Project 1 
import requests
import pandas as pd 
import json

#getting data from API (benchmark 1)
#https://pipedream.com/@pravin/http-api-for-latest-wuhan-coronavirus-data-2019-ncov-p_G6CLVM/readme
url = "https://coronavirus.m.pipedream.net/"
query = {"symbols": "summaryStats"}

# throw error message 
try:
    response = requests.request("GET", url, params=query)
except:
    print('Error: Cannot connect to API')
jsonresponse = response.json()

#formatting data and deleting irrelevant columns (benchmark 3)
dataframe=pd.DataFrame(data=jsonresponse['summaryStats'])
dataframe=dataframe.drop(columns=['china','nonChina'])
dataframe=dataframe.drop('recovered',axis=0)
dataframe=dataframe.T
print(dataframe)

#adding death rate column (benchmark 3)
dataframe['death rate'] = dataframe.apply(lambda row: ((row.deaths/row.confirmed)*100) , axis=1)
dataframe['death rate'] = dataframe['death rate'].round(2).astype(str) + '%'
print(dataframe)

#writing to local disk (benchmark 4)
dataframe.to_csv('covidstats.csv', index= True)
