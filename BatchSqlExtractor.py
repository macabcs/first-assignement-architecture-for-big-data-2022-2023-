from abc import abstractmethod
from helperDT import Database,query,Data
from sql_conn import Sql_conn
import threading
import time

class BatchSqlExtractor:

    def __init__(self,sourceDB: Database, histDb: Database, query : query) -> None: #add paramse for the secondo db, create second database in attribute
        self.oneStreamConnection= self.__connect(sourceDB) #control update time
        self.histDBConnection = self.__connect(histDb)
        self.lastUpdate = 0
        self.queryParams = query

        x = threading.Thread(target= self.__synchronizer)
        x.start()

    def __synchronizer(self):
        while(True):
            while(self.__updateCondtion()):
                self.update()
            time.sleep(60*60*24*1000)

    def update(self):
        listOfQuerys =self.readLog()    # retrieve executed query
        filteredQuerys = self.filterQuery(listOfQuerys)     # remove select query
        refactoredQuerys = self.refactorQuery(filteredQuerys)      # adding timestamp value 
        for query in refactoredQuerys:  
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

    def __firstUpdate(self) -> None: 
        query = f"SELECT{self.queryParams.columns} \
             from {self.queryParams.tables}"
        self.lastUpdate= time.time()
        data = self.__readFromOneStream(query)
        self.__insertHistDatabase(data)
        
    @abstractmethod
    def __readFromOneStream(self, query: str)-> Data: # use OneStream API to execute the query and return the result represented with our Data format
        pass
    
    @abstractmethod
    def __insertHistDatabase(self, data: Data) -> None: #execute insertion in historical database 
        pass

    @abstractmethod
    def __connect(self, database:Database) ->Sql_conn :
        pass
    def filterQuery(listOfQuerys): pass
 #   def read

#class dbConnection:
    #__init__(self, credential):
      #  assert(checkAuthorize()):
        