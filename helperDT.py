class query:
    def __init__(self, listTables, listColumns, listCondition) -> None:
        pass
    def checkInjection(self) -> bool:
        pass

class Data:  #class used to interpret and represent data read from OneStream and to write on the hist databases
    pass

class Database:
    def __init__(self,address,port,user,password) -> None:
        self.address=address
        self.port=port
        self.user=user
        self.password=password
