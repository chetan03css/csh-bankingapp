import mysql.connector
import random

host = 'localhost'
database = 'bankdb'
user = 'root'
password = 'root123'
print("Connecting to database...\n")
con = mysql.connector.connect(host=host, database=database, user=user, password=password)
cur = con.cursor()
if con is not None:
    print("Connected to ", database)
query = "select * from customers"
cur.execute(query)
customers = cur.fetchall()
print(customers[-1][0])
cid=customers[-1][0]
cid=cid[3::1]
ncid=int(cid)+1
print("Next customer id:",ncid)
name=input("Enter name:")
ph=input("Enter nmbr:")
email=input("Enter email:")
loc=input("Enter location:")
uname=email[:email.find("@"):1]
banklist=['okciti','okhdfc','oksbi','okyes','okaxis']
upi=ph+"@"+random.choice(banklist)
print("The upi id is:",upi)
print("The username is:",uname)
#customer=[(ncid,ph,email,loc,uname)]
#query = "INSERT INTO CUSTOMERS VALUES(%s,%s,%s,%s,%s,%s,%s);" 




