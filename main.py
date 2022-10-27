from abc import abstractmethod
from datetime import datetime
from turtle import update
from xmlrpc.client import boolean
from sql_conn import Sql_conn
import threading
import time
class query:
    def __init__(self, listColumn, listTables, listCondition) -> None:
        pass
    def checkInjection(self) -> boolean:
        pass

class Data:  #format to represent data read from OneStream and to be written on the hist databases
    pass
class Database:
    def __init__(self,address,port,user,password) -> None:
        self.address=address
        self.port=port
        self.user=user
        self.password=password
        pass
class BatchSqlExtractor:

    def __init__(self,dataSince,oneStreamDb: Database, histDb: Database, query : query) -> None: #add paramse for the secondo db, create second database in attribute
        self.oneStreamConnection= self.__connect(oneStreamDb) #control update time
        self.histDBConnection = self.__connect(histDb)
        self.lastUpdate = dataSince
        self.queryParams = query

        x = threading.Thread(target= self.__synchronizer)
        x.start()

    def __synchronizer(self): #implement using update method 
        while(True):
            time.sleep(60*60*24*1000)
            while(self.__updateCondtion()):
                update()


    
    def __updateCondition(self) -> bool:  #implement the policy update based on the Month End Closing activities.
        pass

    def __update(self) -> None: #dabase
        updateTo = datetime.today().replace(day=1).timestamp()
        query = f"SELECT{self.queryParams.columns} \
             from {self.queryParams.tables} \
                 where {self.queryParams.conditions} \
                    and timestamp >= {self.lastUpdate} and  timestamp < {updateTo}" #wrote a good query
        self.lastUpdate= datetime.today()
        data = self.__readFromOneStream(query)
        self.__updateCopyDatabase(data)
        #drop da hist data
        
    @abstractmethod
    def __readFromOneStream(self,query:str)-> Data: # use OneStream API to execute the query and return the result represented with our Data format
        pass
    
    @abstractmethod
    def __updateCopyDatabase(self,data :Data) -> None: #execute insertion in historical database
        pass

    @abstractmethod
    def __connect(self, database:Database) ->Sql_conn :
        pass

 #   def read

