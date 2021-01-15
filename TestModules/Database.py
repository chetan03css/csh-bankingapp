import mysql.connector

host = '35.154.90.20'
#host = 'localhost'
database = 'bankdb'
port = 3306
user = 'root'
password = 'root123'

print("Connecting to database...\n")

con = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)


cur = con.cursor()
if con is not None:
    print("Connected to ", database)
query = "show tables"
cur.execute(query)
databases = cur.fetchall()
for db in databases:
    print("Table = ", db)

