'''
@Author : Daniel Gitahi

*This module requires a working internet connection and valid salesforce credentials for the company.
Please contact the IT administrator to acquire the above mentioned requirements if you do not already
have them.

*This Document contains the definition of a ForceConnection class that allows the user to
easily extract data from companies salesforce instance. This module has been customized to
make it easier for shipped and warehoused parts to be retrieved.
    NB.The kits, as stored in salesforce, are identifers that will help the user retrieve individual
    parts. Therefore, a kit is a collection of individual parts.
'''

from simple_salesforce import Salesforce
from urllib.request import urlopen
import numpy as np

class ForceConnection:
    def __init__(self,username=None,password=None,securityToken=None):
        #assign data members
        self.username = username
        self.password = password
        self.securtiyToken = securityToken
        self.err=list()
        self.conn=None
        self.warehousedKits = list()
        self.shippedKits = list()
    def getWarehousedAndShippedKits(self):
        return self.getShippedKits()+self.getWarehousedKits()
    def getError(self):
        if(len(self.err) == 0 ):
            self.err.append("No errors")
        return self.err
    def credentialsProvided(self):
        return ((self.username != None) and
                (self.password != None) and
                (self.securtiyToken != None) and
                (len(self.username.strip()) != 0 ) and
                (len(self.password.strip()) != 0 ) and
                (len(self.securtiyToken) != 0))
    def getShippedKits(self):
        if (self.forceConnect()):
            shippedQry = "SELECT CKSW_BASE__Serial_Number__c FROM CKSW_BASE__Product_Instance__c WHERE Model_Number__c LIKE '%board%' AND Location_Ref__c LIKE '%shipped%'"
            result = self.conn.query_all(shippedQry)
            records = result['records']
            for record in records:
                self.shippedKits.append(record['CKSW_BASE__Serial_Number__c'])
            return self.shippedKits
    #The 'getWarehousedKits' method returns a list of kits identifiers when successfull. Otherwise, it returns False
    def getWarehousedKits(self):
        if(self.forceConnect()):
            warehouseQry = "SELECT CKSW_BASE__Serial_Number__c FROM CKSW_BASE__Product_Instance__c WHERE Model_Number__c LIKE '%board%' AND Location_Ref__c LIKE '%WAREHOUSE%'"
            try:
                result = self.conn.query_all(warehouseQry)
                records = result['records']
                for record in records:
                    self.warehousedKits.append(record['CKSW_BASE__Serial_Number__c'])
                return self.warehousedKits
            except:
                self.err.append("Invalid Query")
                return False
    def networkConnection(self):
        try:
            urlopen("http://www.google.com")
            return True
        except:
            return False

        #verify existence of data members
    def forceConnect(self):
        if(not self.credentialsProvided()):
            self.err.append("Empty Username,password or Security Token")
            return False
        if(not self.networkConnection()):
            self.err.append("No internet Connection")
            return False
        try:
            self.conn = Salesforce(username=self.username,password=self.password,security_token=self.securtiyToken)
            return True
        except:
            self.err.append("Invalid Login Credentials")
            return False




