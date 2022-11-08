from helperDT import credential
from abc import abstractmethod
import threading

class dbAdapter:
    def __init__(self, credentialPath, logPath, structurePath, ip, port,**kwargs):
        self.credentialPath = credentialPath
        self.logPath = logPath
        self.structurePath = structurePath
        self.serverPath = (ip,port)
        self.__init_db(**kwargs)
        x = threading.Thread(target= self.__listener)

    @abstractmethod
    def __init_db(self) : pass

    def __listener(self):  
        """method that wait requests,it expose 3 services (using rest api for example): check credential, getChanges, execute query """
        pass

    def checkCredential(credential : credential):
        pass

    def update(self): pass


