#Actualizar cada vez que cambian los intentss

import random
import json
import pickle
import numpy as np
import nltk

from keras.models import Sequential
from nltk import WordNetLemmatizer
from keras.layers import Dense, Dropout
from keras.optimizers import SGD


lemmantize = WordNetLemmatizer()

intents = json.loads(open("intents.json").read())

palabras = []
clases = []
documentos = []
ignore_letters = ["?", "!", ".", ","]
for intent in intents['intents']:
	for pattern in intent['patterns']:
		word_list = nltk.word_tokenize(pattern)
		palabras.extend(word_list) 
		
		documentos.append(((word_list), intent['tag']))

		if intent['tag'] not in clases:
			clases.append(intent['tag'])

palabras = [lemmantize.lemmatize(word)
		for word in palabras if word not in ignore_letters]
palabras = sorted(set(palabras))

pickle.dump(palabras, open('words.pkl', 'wb'))
pickle.dump(clases, open('classes.pkl', 'wb'))

training = []
output_empty = [0]*len(clases)
for document in documentos:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmantize.lemmatize(
        word.lower()) for word in word_patterns]
    for word in palabras:
        bag.append(1) if word in word_patterns else bag.append(0)
          
    output_row = list(output_empty)
    output_row[clases.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training)
  
train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), 
                activation='softmax'))
  
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1) #note to self make epochs be more 50000000000000
  
model.save("chatbotmodel.h5", hist)
  

print("Yay! El Bot Esta Completo!!")

#Actualizar cada vez que cambian los intentss
