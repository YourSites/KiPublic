# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 10:46:58 2020

@author: dakov
"""

from DBAccess import DBAccess as dba

from APIAccess import APIAccess as apiA


def parseFile(filepath):
    
    with open(filepath, "r") as file:
        
        currentLine = file.readline()
        outputSites = []
        outputSolutions = []
        
        while currentLine != "":
            
            outputSites.append(currentLine[0:currentLine.find(",")])
            outputSolutions.append(currentLine[len(currentLine) - 2])
            
            currentLine = file.readline()
    
    return([outputSites, outputSolutions])



def addDataToTable(dataSites, dataSolutions, dbConnection, table, columns):
    
    dataExtractor = apiA()
    
    for i in range(len(dataSites)):
    
        if dbConnection.checkConnection() is False:
            
            dbConnection.reconnect()
            
    
        if dbConnection.checkForElementInColumn(table, columns[0], dataSites[i]) == []:
        
               
            try:
                
                websiteData = dataExtractor.getDataFromWebsite(dataSites[i], dataSolutions[i])
                
                if dbConnection.checkConnection() is False:
                    
                    try:
                        
                        dbConnection.reconnect()
                        print("Verbinde erneut zum DB Server...")
                    
                    except Exception as e:
                        
                        print(e)
                
                if websiteData is not None: 
                    
                    dbConnection.insertArrayIntoDB(table, columns, websiteData)
                    print("Erfolg! " + dataSites[i] + " zur Datenbank hinzugefügt, noch " + str( len(dataSites) - i) + " verbleibend.")
                    
                else:
                    
                    print("Fehler! Die API hat bei einem Wert ull bekommen!")
                    
                    
            except Exception as e:
                
                print("Beim hinzufügen von " + dataSites[i] + " ist leider der Fehler: " + str(e) + " aufgetreten.")
        else:
            
            print("Eintrag übersprungen! " + dataSites[i] + " ist bereits in der Tabelle!")
            
#Variablen um vorgang zu starten festgelegt
            
fileData = parseFile(input())
print("Liste der Webseiten die durch das Script Laufen:")
print(fileData)
print(str(len(fileData)) + " Seiten!")

siteArray = fileData[0]
solutionArray = fileData[1]

myConnection = dba(")
myTable = ""
myColumns = []

#Script starten

addDataToTable(siteArray, solutionArray, myConnection, myTable, myColumns)
