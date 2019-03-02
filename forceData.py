from simple_salesforce import Salesforce
from urllib.request import urlopen

class ForceConnection:
    def __init__(self,username=None,password=None,securityToken=None):
        #assign data members
        self.username = username
        self.password = password
        self.securtiyToken = securityToken
        self.err=list()
        self.conn=None
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
        if(self.forceConnect()):
            shippedQry=""

        pass

    def getWarehousedKits(self):
        if(self.forceConnect()):
            warehouseQry = "SELECT CKSW_BASE__Serial_Number__c FROM CKSW_BASE__Product_Instance__c WHERE Model_Number__c LIKE '%board%' AND Location_Ref__c LIKE '%WAREHOUSE%'"


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




