import mysql.connector
from bankAPI import *
def login():
    uname=input("Enter your username:")
    pwd=input("Enter your password:")
    query="select * from customers where CUSTOMER_USERNAME='%s' and CUSTOMER_PASSWORD='%s'" %(uname,pwd)
    con=getDBConnection()
    cur=con.cursor()
    cur.execute(query)
    clist=cur.fetchall()
    if len(clist)==0:
        return None
    else:
        return clist



print(login())
        
