Organisation of the code :

3 classes : 
  - wrapper/adapter for DBMs (role : ensure code adaptability even if changes on the level of DBMs)
  - Batch SQL Extractor (role : allow read from web app, define the frequency of querying for changes, call the functionnal methods for getting changes
                        and data, initialise the connection between DBMs and HistDB)
  - DB Connector (role : instantiate the functionnal methods to manipulate the data) 
