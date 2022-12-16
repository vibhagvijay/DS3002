#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:55:19 2022

@author: Skye Jung hsj5sn Vibha Vijay vgv9sn
"""

#importing packages
import json
import csv
import pandas as pd
import numpy as np

# best movie by year as determined by IMDB score and number of votes
file1 = '/Users/skyejung/Desktop/netflix/Best Movie by Year Netflix.csv'

# best movies on Netflix according to the IMDB score and number of votes
file2 = '/Users/skyejung/Desktop/netflix/Best Movies Netflix.csv'

# best TV show by year, as determined by IMDB score and number of votes
file3 = '/Users/skyejung/Desktop/netflix/Best Show by Year Netflix.csv'

# best TV shows on Netflix, as determined by their IMDB score and number of votes
file4 = '/Users/skyejung/Desktop/netflix/Best Shows Netflix.csv'

# information on all of the movies and TV shows available on Netflix as of May 2022
file5 = '/Users/skyejung/Desktop/netflix/raw_titles.csv'

#%%

#reading in the csv and transforming it 
data1 = pd.read_csv(file1)
data1 = data1.iloc[:,1:]
print(data1.head(10))
data1.to_csv('/Users/skyejung/Desktop/netflix/data1.csv')

#reading in the csv and transforming it 
data2 = pd.read_csv(file2)
data2 = data2.iloc[:,1:]
print(data2.head(10))
data2.to_csv('/Users/skyejung/Desktop/netflix/data2.csv')

#reading in the csv and transforming it 
data3 = pd.read_csv(file3)
data3 = data3.iloc[:,1:]
print(data3.head(10))
data3.to_csv('/Users/skyejung/Desktop/netflix/data3.csv')

#reading in the csv and transforming it 
data4 = pd.read_csv(file4)
data4 = data4.iloc[:,1:]
print(data4.head(10))
data4.to_csv('/Users/skyejung/Desktop/netflix/data4.csv')


#%%

#testing and merging the transformed data
test2 = data2.iloc[:,[0,3,4]]
qdata1 = pd.merge(data1, test2, on='TITLE')
qdata1.to_csv('/Users/skyejung/Desktop/netflix/qdata1.csv')

test4 = data4.iloc[:,[0,3,4]]
qdata2 = pd.merge(data3, test4, on='TITLE')
qdata2.to_csv('/Users/skyejung/Desktop/netflix/qdata2.csv')

#creating a dataframe and converting to a csv
frames = [newdata1,newdata2]
df = pd.concat(frames)
df.to_csv('/Users/skyejung/Desktop/netflix/project2data.csv')

#casting the opened data files into a new csv
dfcsv = open('/Users/skyejung/Desktop/netflix/project2data.csv','r')
dfjson = open('/Users/skyejung/Desktop/netflix/project2data.json','w')
variables = ("title","release_year","score","main_genre","in_production","number_of_votes","duration","movie_tv","number_of_seasons")
reader = csv.DictReader(dfcsv,variables)

for each in reader:
    json.dump(each,dfjson)
    data1json.write('\n')
    json.dumps(each,sort_keys=False,indent=4,separators=(',',': '))

#%%

## Ten Questions

# Most votes for top movies of all years? newdata1
# Most votes for top show of year? newdata2
# Highest imdb score in past 10 years? newdata1
# Highest imdb score past 10 years? newdata2
# Average Movie runtime for top movies in past 10 years?
# Average show runtime for top shows in past 10 years? newdata2
# Genre of top movie of 2022? newdata1
# Genre of top show of 2022? newdata2
# Average Number of seasons of top show of past 10 years? newdata2
# Lowest scoring "top" movie AND year















