Organisation of the code :

3 classes : 
  - wrapper/adapter for DBMs (role : ensure code adaptability even if changes on the level of DBMs)
  - Batch SQL Extractor (role : allow read from web app, define the frequency of querying for changes, call the functionnal methods for getting changes
                        and data, initialise the connection between DBMs and HistDB)
  - DB Connector (role : instantiate the functionnal methods to manipulate the data) 

------DESCRIPTION OF THE ARCHITECTURE------------

- DBMs side : the DBMs contains three main elements : the transaction data (the bigger batch of data to handle, the one at the heart of the problem), the customer table (smallest table, rarely changed/updated) and a log table that adds a line for each operation done on the transaction and customer table. 

The class that we implement around this DB is a wrapper. It's role is to allow that even in the event of a change in the code of the DB we ensure that the communication and the data transaction task still functions on our server and web app side. 

    METHODS IN THE DBWRAPPER (to be updated by Davide)
      - 
      
BATCH SQL EXTRACTOR : that is the interface that allows a smooth transaction of data between the external DB and the company's Db. It contains the methods to instantiate and handle the connection to the external DB aswell as the method to update the data on the company's side when needed

    METHODS IN THE EXTRACTOR 
    
    - dbConnector :
    - getChanges :
    - execQuery : 
    - update : 
    - firstUpdate : 
    

WEB APP : This is the side where we need the data handled and displayed to the user. The only method that we need on that side is a read method to get the data from the historical DB. the rest of the data treatment is handled by the web app. 
