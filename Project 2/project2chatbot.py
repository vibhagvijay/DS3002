#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:24:45 2022

@author: Skye Jung hsj5sn and Vibha Vijay vgv9sn

"""
#importing packages 
import os
import datetime
import pymongo
import pprint
import pandas as pd


#setting up the server connection 
host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"
atlas_user_name = "m001-student"
atlas_password = "m001-mongodb-basics"

conn_str = {
    "local" : f"mongodb://{host_name}:{port}/",
    "atlas" : f"mongodb+srv://{atlas_user_name}:{atlas_password}@{atlas_cluster_name}.zibbf.mongodb.net/{atlas_default_dbname}"
}

client = pymongo.MongoClient(conn_str["local"])

db_name = "Netflix"
db = client[db_name]
movies = db.movies
shows = db.shows


from csv import DictReader
# open file in read mode
with open("/Users/skyejung/Desktop/netflix/project2data.csv", 'r') as f:
     
    dict_reader = DictReader(f)
     
    list_of_movies_and_tv_shows = list(dict_reader)
   

for item in list_of_movies_and_tv_shows:
    if item['movie_tv'] == "movie":
        movies.insert_one(item)
    else:
        shows.insert_one(item)

#%%
import nltk 
import discord
nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
# pip install tflearn
# pip install tensorflow
import tflearn
import tensorflow as tf
import random
import json
import pickle


with open("/Users/skyejung/Desktop/netflix/questions.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)


#fitting and testing the model 
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

    
    
#building the function to cast the words in an array
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


#building the chat function
def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    if tg['tag'] == 'question1':
                        movie = list(movies.find().sort("NUMBER_OF_VOTES"))[-1]
                        print(movie['TITLE'] + ' released in ' + movie['RELEASE_YEAR'])
                    
                    if tg['tag'] == 'question2':
                        show = list(shows.find().sort("NUMBER_OF_VOTES"))[-1]
                        print(show['TITLE'] + ' released in ' + show['RELEASE_YEAR'])
                    
                    if tg['tag'] == 'question3':
                        movie = list(movies.find().sort("SCORE"))[-1]
                        print(movie['TITLE'] + ' with score ' + movie['SCORE'] + ' released in ' + movie['RELEASE_YEAR'])
                    
                    if tg['tag'] == 'question4':
                        show = list(shows.find().sort("NUMBER_OF_VOTES"))[-1]
                        print(show['TITLE'] + ' with score ' + show['SCORE'] + ' released in ' + show['RELEASE_YEAR'])
                    
                    if tg['tag'] == 'question5':
                        list_of_movies = list(movies.find())
                        runtime_sum = 0
                        for movie in list_of_movies:
                            runtime_sum += float(movie['DURATION'])
                        print(str(runtime_sum / len(list_of_movies)) + " minutes")
                    
                    if tg['tag'] == 'question6':
                        list_of_shows = list(shows.find())
                        runtime_sum = 0
                        for show in list_of_shows:
                            runtime_sum += float(show['DURATION'])
                        print(str(runtime_sum / len(list_of_shows)) + " minutes")
                        
                    if tg['tag'] == 'question7':
                        list_of_movies = list(movies.find())
                        genre_dict = {}
                        for movie in list_of_movies:
                            try:
                                genre_dict[movie['MAIN_GENRE']] += 1
                            except:
                                genre_dict[movie['MAIN_GENRE']] = 1
                                
                        print(max(genre_dict, key=genre_dict.get))
                        
                    if tg['tag'] == 'question8':
                        list_of_shows = list(shows.find())
                        genre_dict = {}
                        for show in list_of_shows:
                            try:
                                genre_dict[show['MAIN_GENRE']] += 1
                            except:
                                genre_dict[show['MAIN_GENRE']] = 1
                                
                        print(max(genre_dict, key=genre_dict.get))
                        
                    if tg['tag'] == 'question9':
                        list_of_shows = list(shows.find())
                        seasons_sum = 0
                        for show in list_of_shows:
                            seasons_sum += float(show['NUMBER_OF_SEASONS'])
                        print(str(seasons_sum / len(list_of_shows)) + " seasons")
                        
                    if tg['tag'] == 'question10':
                        lowest_scoring_movie = list(movies.find().sort("SCORE"))[0]
                        print(lowest_scoring_movie["TITLE"] + " released in " + movie['RELEASE_YEAR'])

                    
                    
        else:
            print("I didnt get that. Can you explain or try again.")
chat()


