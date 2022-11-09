from abc import abstractmethod
from typing import Tuple,Sequence


class query:
    def __init__(self, string) -> None:
        self.operation, self.table, self.listColumns, self.listCondition = self.ParseString(string)
    @abstractmethod
    def checkSqlInjection(self) -> bool:
        pass
    @abstractmethod
    def parseString(self, string)-> Tuple[str,str,Sequence[str],Sequence[str]] :pass
    @abstractmethod
    def toString(self) -> str :pass 

class Data:  #class used to interpret and represent data read from operationalDB and to write on the hist databases
    pass

class DatabaseCredential:
    def __init__(self,address,port,user,password) -> None:
        self.address=address
        self.port=port
        self.user=user
        self.password=password
