# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 09:28:20 2020

@author: lakju
"""

import requests
import json

class APIAccess:
    
    
    def __init__(self):
        
        self.api1 = ""
        self.api2 = ""
    
    def sslCertificate(self, url):
        
        
        checkURL = url[0:5]
        
        if(checkURL == "https"):
            
            return "1"
        
        return "0"
    
    
    def getDataFromWebsite(self, website, solution):
        
        api = self.api1 + website + self.api2
        

        response = requests.get(api, timeout=120)
        response = response.text.encode().decode('utf-8-sig')
        data = json.loads(response)
        
        output = [website, self.sslCertificate(website), str(]
        return output if None not in output else None

        

    
   
    
    
