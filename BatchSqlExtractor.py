from abc import abstractmethod
from helperDT import Database,query,Data
import threading
import time

class DBconnection:
    def execute_query(self, query): pass
    def getChanges(self,timestamp):pass
    
class BatchSqlExtractor:

    def __init__(self,sourceDB: Database, histDb: Database) -> None: #add paramse for the secondo db, create second database in attribute
        self.oneStreamConnection= self.__connect(sourceDB) #control update time
        self.histDBConnection = self.__connect(histDb)
        self.lastUpdate = 0  #get the fresh changes
        self.__fullUpdate()
        x = threading.Thread(target= self.__synchronizer)
        x.start()

    def __synchronizer(self):
        while(True):
            while(self.__updateCondtion()):
                self.update()
            time.sleep(60*60*24*1000)

    def update(self): #get the log that goes from the last ts
        listOfQuerys = self.readLog()    # retrieve executed query
        for query in listOfQuerys:  
             self.histDBConnection.execute_query(query)     #execute every new query (insert, update and delete)
              
        self.lastUpdate = time.time()   # update lastUpdate attribute to actual timestamp 


    @abstractmethod
    def readLog(self): 
        #define this method such that it makes a SELECT query to the log table of the original database
        #and return a list of string pair ( query , timestamp ) 
        #this method has to select rows that have timestamp >= self.lastUpdate (initially zero because we want to take all data at the beginning)
        pass

    @abstractmethod
    def __updateCondition(self) -> bool:  #implement the update policy based on the Month End Closing activities and the OneStream's load balance 
        pass

    def __fullUpdate(self) -> None: #He have to do a full copy of operationDb and report it on histDb, and update the lastUpdate field
        query = f"SELECT{self.queryParams.columns} \
             from {self.queryParams.tables}"
        self.lastUpdate= time.time()
        data = self.__readFromOneStream(query)
        self.__insertHistDatabase(data)
        
    @abstractmethod
    def __connect(self, database:Database) -> DBconnection :
        pass


