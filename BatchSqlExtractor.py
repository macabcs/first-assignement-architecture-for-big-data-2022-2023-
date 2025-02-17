from abc import abstractmethod
from helperDT import Database, query, Data
import threading
import time


class DBconnection:
    def execute_query(self, queryWithTime): pass

    def getChanges(self, timestamp): pass
    
    def readAllData(self, database:DB): pass #method for the initial copy of the DB
    
    def writeAllData(self, database:DB): pass #method for the initial copy of the DB 
    
    


class BatchSqlExtractor:

    def __init__(self, sourceDB: Database,
                 histDb: Database) -> None:  # add paramse for the secondo db, create second database in attribute
        self.oneStreamConnection = self.__connect(sourceDB)  # control update time
        self.histDBConnection = self.__connect(histDb)
        self.lastUpdate = 0  # get the fresh changes
        self.__fullUpdate()
        x = threading.Thread(target=self.__synchronizer)
        x.start()

    def __synchronizer(self):
        while (True):
            while (self.__updateCondtion()):
                self.update()
            time.sleep(60 * 60 * 24 * 1000)

    """ get the log that goes from the last ts
    listOfQueries -  [[timestamp1,query1], [timestamp2,query2]]
    getChanges - retrieve executed query """
    def update(self):
        listOfQueries = DBconnection.getChanges(self, self.lastUpdate)
        for queryWithTime in listOfQueries:
            try:
                # execute every new query (insert, update and delete)
                self.histDBConnection.execute_query(queryWithTime)
                self.lastUpdate = queryWithTime[0]
            except:
                print("db exception occurred.")
                break

    @abstractmethod
    def __updateCondition(
            self) -> bool:  # implement the update policy based on the Month End Closing activities and the OneStream's load balance
        pass

    def firstUpdate(self, database:Source, database:Target): # this method does the initial copy to the histDb
        
        self.__connnect(self, database: Source) #here we connect to the source database
        self.__connect(self, database: Target) #and connect to the target histDb 
        
        try:
            readFromSource(self, database: Source)
            writeToTarget(self, database: Target) 
            #execution of the data copy
        except:
            print("failure reading from source or writing on target")
            break
            
    @abstractmethod
    def __connect(self, database: Database) -> DBconnection:
        pass
