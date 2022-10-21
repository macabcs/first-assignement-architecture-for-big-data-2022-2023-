from abc import abstractmethod
from concurrent.futures import thread
from dataclasses import dataclass
from turtle import update
from xmlrpc.client import boolean
from sql_conn import Sql_conn
import threading

class query:
    def __init__(self, listColumn, listTables, listCondition) -> None:
        pass
    def checkInjection(self) -> boolean:
        pass

class Data:  #format to represent data read from OneStream and to be written on the hist databases
    pass

class BatchSqlExtractor:

    def __init__(self,updateTime,adress,port,credential,query) -> None: #add paramse for the secondo db, create second database in attribute
        self.database_connection = self.connect(adress,port,credential) #control update time
        self.update = updateTime
        self.queryParams = query
        x = threading.Thread(target= self.synchronizer)
        x.start()

    def synchronizer(self):
        while(self.orariodiadesso> self.lastupdate+self.updateTime): #sistemo ma idea è questa
            self.update()

    def __first_update(self) -> None:
        check_update() #creare update per capire
        query = f"SELECT * from TABLENAME when timestamp >= {self.update}" #wrote a good query
        data = self.__readFromOneStream(query)
        self.__update_copy_dataset(data)
        #drop da hist data
        
    @abstractmethod
    def __readFromOneStream(self,query)-> Data:
        pass
    
    @abstractmethod
    def __update_copy_dataset(self,data :Data) -> None:
        pass

    @abstractmethod
    def connect(self,address,port,credential) ->Sql_conn :
        pass

pippo = BatchSqlExtractor()
pippo.readFromOneStream()

