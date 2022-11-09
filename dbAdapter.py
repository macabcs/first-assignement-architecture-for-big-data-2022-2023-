from helperDT import credential,query
from typing import Tuple,Sequence
from pathlib import Path
from abc import abstractmethod
import threading
import time

class dbAdapter:
    def __init__(self, credentialPath, logPath, structurePath, ip, port,**kwargs):
        self.credentialPath = credentialPath
        self.logPath = logPath
        self.structurePath = structurePath
        self.serverPath = (ip,port)
        self.__init_db(**kwargs)
        self.operationDict = {"INSERT" : lambda self,query: self.AdInsert(query),
                              "UPDATE" : lambda self,query: self.AdUpdate(query),
                              "DELETE" : lambda self,query: self.AdDelete(query),
                              "SELECT" : lambda self,query: self.AdSelect(query)}
        self. serverThread = threading.Thread(target= self.__listener)
        self.serverThread.start()


    @abstractmethod
    def __init_db(self) : pass
    @abstractmethod
    def __listener(self):  
        """method that wait requests,it expose at least 3 services (using rest api for example): getChanges, executeQuery and getDbStructure"""
        pass
    
    def executeQuery(self,query:query,credential : credential) -> str:
        allowed,wrongCredentialMessage = self.__checkCredential(query,credential)
        if(not allowed): return wrongCredentialMessage
        if(not self.__checkCredential(query,credential)[0]): return "wrong credential"
        error,status = self.__dbExecuteQuery(query,credential) #do the query on db and check if all is ok, if not we return an error to the listener
        if(error): return status
        self.operationDict[query.operation](self,query) #we use this call to do some operations after the query is done on the db. in our idea these call can be used to save operation
                                                        #logs to CDC 
        return status
    @abstractmethod
    def __checkCredential(self,query,credential)-> Tuple[bool,str] : pass #we want to have a check credential on the adapter because permette di ottenere un controllo 
                                                        #più fine-grained sugli accessi e di creare una politica degli acessi che sia indipendente da quella del db.
                                                        #Nel caso la politica degli accessi del db specifico vada già bene si può far tornare sempre true
    @abstractmethod
    def __dbExecuteQuery(self,query,credential) -> Tuple[bool,str] :pass

    def getChanges(self,tableList,credential,sync)-> dict :
        allowed,wrongCredentialMessage = self.__checkReadCredential(tableList,credential)
        if(not allowed): return wrongCredentialMessage
        result= {}
        for table in tableList:
            result[table] = (self.__getTableChanges(table,sync[table]))
        return result
   
    @abstractmethod
    def __getTableChanges(self,table,sync) -> Sequence[query] : pass  #this method use the sync information to extract the fresh query that are done on the db. The sync information can for be example the lastUpdate ts
                                                                      #so i want to return, for that table all the query that are saved in the logs with ts grater than sync. Another option can be to  differentiate registry and log tables and for
                                                                      #the registry tables send in sync the hash of table (for each row hash(keyCol) and hash(valueCol) and extract the query computing the difference from the same hash calculated on
                                                                      #DB tables. 

    @abstractmethod
    def __checkReadCredendial(self,tables,credential) -> Tuple[bool,str] : pass

    @abstractmethod
    def getStructure(self) -> dict : pass #return the struct of the db in form of dictionary

    def __AdInsert(self,query) : 
        self.__savelog(query)
    
    def __AdUpdate(self,query):
        self.__savelog(query)
    
    def __AdDelete(self,query):
        self.__savelog(query)
    
    def __AdSelect(self,query): pass #we don't like build 4 identical methods but the idea is that
                                    #if anyone wants to modify one of these in a concrete class he can extends only that specific
                                    #method. These methods are used to do some additional operation after that a specific
                                    #type of query is done on the db (look executeQuery and operationDict).
                                

    def __saveLog(self,query:query):   
        savePath = Path(self.logPath / query.table / f"{time.localtime()}.log" )
        with open(savePath) as logfile:
            logfile.write(query.toString())


   




