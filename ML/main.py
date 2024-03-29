#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Imports
import nltk
#nltk.download('punkt')
import os
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

#Loading Data
with open("intents.json") as file:
	data = json.load(file)


# In[ ]:


#Initializing empty lists
words = []
labels = []
docs_x = []
docs_y = []

#Looping through our data
for intent in data['intents']:
	for pattern in intent['patterns']:
		pattern = pattern.lower()
    		#Creating a list of words
		wrds = nltk.word_tokenize(pattern)
		words.extend(wrds)
		docs_x.append(wrds)
		docs_y.append(intent['tag'])

	if intent['tag'] not in labels:
	  labels.append(intent['tag'])


# In[ ]:


stemmer = LancasterStemmer()
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]
for x,doc in enumerate(docs_x):
	bag = []
	wrds = [stemmer.stem(w) for w in doc]
	for w in words:
		if w in wrds:
			bag.append(1)
		else:
			bag.append(0)
	output_row = out_empty[:]
	output_row[labels.index(docs_y[x])] = 1
	training.append(bag)
	output.append(output_row)
#Converting training data into NumPy arrays
training = np.array(training)
output = np.array(output)

#Saving data to disk
with open("data.pickle","wb") as f:
	pickle.dump((words, labels, training, output),f)


# In[ ]:


# tf.reset_default_graph()

net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


# In[ ]:


model.fit(training, output, n_epoch = 200, batch_size = 8, show_metric = True)
model.save("model.tflearn")


# In[ ]:




