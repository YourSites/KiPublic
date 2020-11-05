# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 08:08:17 2020

@author: Tomislav Bosnjakovic
"""

import tensorflow as tf
import numpy as np
from DBAccess import DBAccess as dba


def convertArray(inputArray):

    outputArray = [[0 for x in range(1)] for y in range(len(inputArray))]

    for i in range(len(inputArray)):

        outputArray[i][0] = inputArray[i]

    return outputArray


db = dba("")
inputSpalten = []
outputSpalte = ""
tabelle = ""

# Eingabemuster
inputMuster = np.array(db.getNormalizedTable(tabelle, inputSpalten))
print ("Daten: ")
print (inputMuster)



# Ausgabemuster: AND
outputMuster = np.array(convertArray(db.getColumn(tabelle, outputSpalte)))
print ("Antwort: ")
print (outputMuster)


# Model erstellen
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(3, input_dim=len(inputSpalten), activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(15, input_dim=len(inputSpalten), activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))

# Model compilieren
model.compile(loss='mean_squared_error', optimizer='Adam')

# Model fuer n Epochen trainieren
epochenAnzahl = 2500
model.fit(x=inputMuster, y=outputMuster, epochs = epochenAnzahl, verbose=0)


# Model testen
print("Durch tensorflow erreichte Mustererkennung:")
outputAI = np.array(model.predict(inputMuster));


print(outputAI)
