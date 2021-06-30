# ChangeDupInSQL
## Package:
Python == 3.7  
mysql==0.0.3  
mysql-connector-python==8.0.25  
mysqlclient==2.0.3  
numpy==1.21.0  
pandas==1.2.5  
protobuf==3.17.3  
pyodbc==4.0.30  
python-dateutil==2.8.1  
pytz==2021.1  
six==1.16.0  

This is script to modfiy specific property for duplicated row(depands on certain value);
In our case, our target table is **t_problem** ,we depands on title/row\[0\] to idenfy row and then modify properity bank_request/row\[37\].

## Config
Make sure you create **config.py** under same folder as **ChangeDupInSQL**
```
# config.py
config = {'user':'root', 'password':'xxxx','host':'localhost','database':'target_db'}
```

## Install 

1. Create venv
```console
$ python3 -m venv /path/to/new/virtual/environment
$ venv/Scripts/activate
```
2. Install package
```console
$(env) pip install -r requirements.txt
```
If error occur, modify requirements version so they matches.  
Also for mysqlclient, you have to go to download specific package and install that.
[link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)


3. Test connection
make sure you can connect your SQL with SQL command line
``` console
$(env) py -m unittest ChangeDupInSQLTest.py
```
and run test to make sure u you can connect SQL in python

4. Run the script
```console
$(env) py ChangeDupInSQL.py
```

5. Check Log
check Log if there are any errors.
