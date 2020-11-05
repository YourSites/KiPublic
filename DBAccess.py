"""
Klasse die Anbindung zu einer Datenbank möglich macht, und Werte für Künstliche Intelligenzen normalisieren kann
@author: Tomislav Bosnjakovic
"""


import mysql.connector as mc

class DBAccess:
    
    def __init__(self, hostname, db, username, pw):
        
        """
        Konstruktor für DBAccess, Verbindet sich mit Datenbank und erstellt einen Cursor zum Quarrien
        
        Parameters:
            
            hostname (String): Hostname des Datenbankanbieters
            db (String): Datenbank mit der man sich verbinden möchte
            username (String): Username der zum Log-In benutzt wird
            pw (String): Passwort das zum Log-In benutzt wird
            
        """
        
        self.connection = mc.connect(user = username, password = pw, host = hostname, database = db)
        self.cursor = self.connection.cursor()    
    
    
    def checkConnection(self):
        
        return self.connection.is_connected()
    
    def reconnect(self):
        
        self.connection.reconnect()
    
    
    def getBiggestNumber(self, table, col): 
        
        """
        Methode um die groesste Nummer einer Spalte in einer Tabelle zu erhalten
        
        Parameters:
            
            table (String): Die anzusteuernde Tabelle
            col (String): Die anzusteuernde Spalte
        
        Returns:
            
            (number): Groesste Zahl der Spalte
        
        """
        
        self.cursor.execute("SELECT " + col + " FROM " + table + " ORDER BY " + col + " DESC LIMIT 1")
        return self.cursor.fetchone()[0]
    
    
    
    def getTableLength(self, table):
        
        """
        Methode um die Anzahl der Eintraege einer Tabelle zu erhalten
        
        Parameters:
            table (String): Die anzusteuernde Tabelle
        
        Returns:
            (int): Anzahl der Einträge der Tabelle
        """
        
        self.cursor.execute("SELECT COUNT(*) FROM " + table)
        
        return self.cursor.fetchone()[0]
    
    
    
    def getColumn(self, table, col):
        
        """
        Methode um eine ganze Spalte auszulesen
        
        Parameters:
            
            table (String): Die anzusteuernde Tabelle
            col (String): Die anzusteuernde Spalte
            
        Returns:
            
            (Array): Der Wert der angegeben Spalte für alle Einträger der Tabelle
            
        """
        
        self.cursor.execute("SELECT " + col + " FROM " + table)
        
        cols = []
        column = self.cursor.fetchone()
        
        while column is not None:
            
            cols.append(column[0])
            column = self.cursor.fetchone()
        
        return cols    
    
    
    
    def getNormalizedValuesFromColumn(self, table, col):
        
        """
        Methode um alle Werte einer Spalte zu normalisieren
        
        Parameters:
            table (String): Die anzusteuernde Tabelle
            col (String): Die anzusteuernde Spalte
            
        Returns:
            (Array): Normalisierte Werte der angegeben Spalte
        """
        
        groesteZahl = self.getBiggestNumber(table, col)
        datenSpalte = self.getColumn(table, col)
        
        normalizedValues = []
        
        if groesteZahl >= 1:
            
            for i in range(len(datenSpalte)):
            
                normalizedValues.append(datenSpalte[i] / groesteZahl)
            
        
        else:
            
            for i in range(len(datenSpalte)):
            
                normalizedValues[i].append(datenSpalte[i])
            
        return normalizedValues
        

    def getNormalizedTable(self, table, columns):
        
        """
        Methode um eine ganze Tabelle zu normalisieren
        
        Parameters:
            
            table (String): Die anzusteuernde Tabelle
            columns (StringArray): Alle Spalten die normalisiert werden sollen
        
        Returns:
            
            (2DArray): Normalisierte Tabelle; Jeder Array enthält eine Reihe
            
        """
        
        normalizedColumn = []
        normalizedTable = [[0 for x in range(len(columns))] for y in range(self.getTableLength(table))] 
        
        for i in range(len(columns)):
            
            normalizedColumn = self.getNormalizedValuesFromColumn(table, columns[i])
            
            for j in range(len(normalizedColumn)):
                
                normalizedTable[j][i] = normalizedColumn[j]
        
        return normalizedTable
    
    def checkForElementInColumn(self, table, column, element):
        
       self.cursor.execute("SELECT " + column + " FROM " + table + " WHERE " + column + " = '" + element + "'") 
       awnser = self.cursor.fetchall()
       
       
       return awnser
    
    def insertArrayIntoDB (self, table, columns, inputs):
        """
        Methode um Array mit eigenschaften einer Webseite in die Datenbank einzufügen
        
        Parameters:
            
            table(String): Die anzusteuernde Tabelle
            columns(StringArray): Alle Spalten in die Werte eingetragen werden sollen
            inputs(StringArray): Daten die in die jeweilige Spalte eingetragen werden sollen
        
        """
        
        sql = "INSERT INTO " + table + " ("
        
        for i in range(len(columns)):
            
            if i is not (len(columns) - 1):
                
                sql += columns[i] + ", "
                
            else:
                
                sql += columns[i]
        
        sql += ") VALUES ("
        
        for i in range(len(inputs)):
            
            if i is not len(inputs) - 1:
                
                sql += "'" + inputs[i] + "'" + ", "
                
            else:
                
                sql += "'" + inputs[i] + "'"
        
        sql += ")"
        
        self.cursor.execute(sql)  
        self.connection.commit()   
        
