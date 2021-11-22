#!/usr/bin/env python
# coding: utf-8

# In[3]:


import nltk
import datetime
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle


# In[ ]:





# In[ ]:


stemmer = LancasterStemmer()


with open("intents.json") as file:
	data = json.load(file)
with open("data.pickle","rb") as f:
	words, labels, training, output = pickle.load(f)

#Function to process input
def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]
	
	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i,w in enumerate(words):
			if w == se:
				bag[i] = 1

	return np.array(bag)

# tf.reset_default_graph()

net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)

#Loading existing model from disk
model = tflearn.DNN(net)
model.load("model.tflearn")


def predict(message):
	results = model.predict([bag_of_words(message,words)])[0]
	result_index = np.argmax(results)
	tag = labels[result_index]
	return tag
	


# message = "mess timings "
# results = model.predict([bag_of_words(message,words)])[0]
# result_index = np.argmax(results)
# tag = labels[result_index]
# temp ={}
# for i,ival in enumerate(labels):
#     temp[ival]=results[i]
# temp = sorted(temp.items(), key =
#              lambda kv:(kv[1], kv[0]))
# for i in temp:
#     print(i[0],i[1])

# print(results[result_index],tag)


while(True):
	print("Q: ")
	message = input()
	print("A: "+predict(message))