import os
import nltk
import datetime
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

stemmer = LancasterStemmer()
# with open(os.path.join(BASE_DIR,'chat','intents.json')) as file:
# 	data = json.load(file)
with open(os.path.join(BASE_DIR,'chat','data.pickle'),"rb") as f:
# with open("./data.pickle","rb") as f:
	words, labels, training, output = pickle.load(f)

def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]
	
	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i,w in enumerate(words):
			if w == se:
				bag[i] = 1

	return np.array(bag)


net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
net = tflearn.regression(net)

#Loading existing model from disk
model = tflearn.DNN(net)
model.load(os.path.join(BASE_DIR,'chat',"model.tflearn"))

def predict(message):
	results = model.predict([bag_of_words(message,words)])[0]
	result_index = np.argmax(results)
	tag = labels[result_index]
	return tag