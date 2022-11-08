from abc import abstractmethod

class query:
    def __init__(self, string) -> None:
        self.operation, self.listTables, self.listColumns, self.listCondition = self.ParseString(string)
    @abstractmethod
    def checkSqlInjection(self) -> bool:
        pass
    @abstractmethod
    def parseString(self, string): pass

class Data:  #class used to interpret and represent data read from OneStream and to write on the hist databases
    pass
class DatabaseCredential:
    def __init__(self,address,port,user,password) -> None:
        self.address=address
        self.port=port
        self.user=user
        self.password=password
