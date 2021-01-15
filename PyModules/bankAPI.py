import mysql.connector
import random
from os import  system

def getDBConnection():
    host = '35.154.90.20'
    #host = 'localhost'
    port = 3306
    database = 'bankdb'
    user = 'root'
    password = '' #somepassword
    con = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)
    cur = con.cursor()
    if con is not None:
        return con
    else:
        return None


# Function Definitions
def openNewBankAccount():
    print("Welcome to City Bank.\nTo open a new bank account, please enter the details:")
    name = input("Enter Your Name:")
    phone = input("Enter Your Phone Number +91-")
    email = input("Enter Your Email ID:")
    city = input("Enter Your Current City:")
    uname = email[0:email.find("@"):1]
    pflag = 1
    upasswd = ' '
    while pflag:
        upasswd = input("Please enter your password:")
        rupasswd = input("Please re-enter your password to confirm:")

        if upasswd == rupasswd:
            pflag = 0
        else:
            print("Passwords Did'nt Match, please try again.")
            pflag = 1

    con = getDBConnection()
    cursor = con.cursor()
    query = "SELECT CUSTOMER_ID from CUSTOMERS;"
    cursor.execute(query)
    lCustomer = cursor.fetchall()
    # print(lCustomer[-1][0])
    if len(lCustomer)==0:
        cid = 'ACB1000000'
    else:
        cid = lCustomer[-1][0]

    ncid = int(cid[3::1])
    ncid = ncid + 1
    ncid = "ACB" + str(ncid)

    # print(ncid)
    query = "SELECT ACCOUNT_NUMBER from ACCOUNTS;"
    cursor.execute(query)
    lAccountNum = cursor.fetchall()
    if len(lAccountNum)==0:
        accnumber = '1000000000'
    else:
        accnumber = lAccountNum[-1][0]

    accnumber = str(int(accnumber) + 1)  # autogen acc num
    print("Choose Your Account Type:")
    print("1.Savings 2.Current")
    opt = int(input("Choose an option:"))
    if opt == 1:
        accType = "SAVINGS"
    elif opt == 2:
        accType = "CURRENT"
    else:
        accType = "SAVINGS"
    oBalance = input("Please enter your seed balance amount :")
    banksList = ["okicici", "okhdfc", "okaxis", "ybl", "oksbi"]
    upID = phone + "@" + random.choice(banksList)
    custData = [(ncid, name, phone, email, city, uname, upasswd)]
    accData = [(accnumber, ncid, accType, oBalance, upID, "ACTIVE")]

    '''print("Please confirm your details before creating the account:")
    print("Name :{}\nPhone:{}\nEmail ID:{}\nCity:{}".format(name, phone, email, city))
    print("Account Type:{}\nOpening Balance:Rs {}/-".format(accType, oBalance))
    opt = int(input("Do you want to Proceed? : 1.Yes 2.No"))
    oFlag=0
    if opt==1:
        oFlag=1
    else:
        oFlag=0
    '''

    # INSERTING INTO DATABASE
    cCustQuery = "INSERT INTO CUSTOMERS VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor = con.cursor()
    cursor.executemany(cCustQuery, custData)
    cAccountQuery = "INSERT INTO ACCOUNTS VALUES(%s,%s,%s,%s,%s,%s)"
    cursor = con.cursor()
    cursor.executemany(cAccountQuery, accData)
    con.commit()
    cursor = con.cursor()
    cursor.execute("SELECT * from CUSTOMERS WHERE CUSTOMER_ID='%s'" % ncid)
    custResult = cursor.fetchall()
    cursor.execute("SELECT * from ACCOUNTS WHERE ACCOUNT_NUMBER='%s'" % accnumber)
    accResult = cursor.fetchall()
    system('cls')
    if custResult is not None and accResult is not None:
        print("Your Account Has Been Successfully Created")
        print("Personal Details :\n--------------------")
        print("Username : {}".format(custResult[0][5]))
        print("Password : {}".format(custResult[0][6]))
        print("Account Details :\n--------------------")
        print("CustomerID : {}".format(accResult[0][1]))
        print("Account Number : {}".format(accResult[0][0]))
        print("Account Type : {}".format(accResult[0][2]))
        print("Opening Balance : {}".format(accResult[0][3]))
        print("UPI ID : {}".format(accResult[0][4]))
        print("Account Status : {}".format(accResult[0][5]))

    else:
        print("There was an error creating your account.")


def closeBankAccount(accountNumber):
    con = getDBConnection()
    cursor = con.cursor()

    cursor.execute("SELECT * from ACCOUNTS WHERE ACCOUNT_NUMBER='%s'" % accountNumber)
    custResult = cursor.fetchall()
    cursor.execute("UPDATE ACCOUNTS SET ACCOUNT_STATUS='CLOSED' where ACCOUNT_NUMBER='%s'" % accountNumber)
    con.commit()
    cursor.execute("SELECT * from ACCOUNTS WHERE ACCOUNT_NUMBER='%s'" % accountNumber)
    status = cursor.fetchall()

    if len(status)!=0 and status[0][5] == 'CLOSED':
        print("ACCOUNT CLOSED SUCCESSFULLY.")
    else:
        print("CLOSE ACCOUNT FAILED ! Please contact the Bank.")

def validateAccountNumber(accountNumber):
    con=getDBConnection()
    cur = con.cursor()
    query = "SELECT CUSTOMER_ID from ACCOUNTS where ACCOUNT_NUMBER='%s'"%accountNumber
    cur.execute(query)
    cList = cur.fetchall()
    if len(cList) == 0:
        return False
    else:
        return True

def getAccountNumber(customerID):
    con=getDBConnection()
    cur = con.cursor()
    query = "SELECT ACCOUNT_NUMBER from ACCOUNTS where CUSTOMER_ID='%s'"%customerID
    cur.execute(query)
    aList = cur.fetchall()
    return aList[0][0]

def getAccountBalance(accountNumber):
    con=getDBConnection()
    cur=con.cursor()
    query="SELECT ACCOUNT_BALANCE FROM ACCOUNTS WHERE ACCOUNT_NUMBER='%s'" %(accountNumber)
    cur.execute(query)
    blist=cur.fetchall()
    bal=int(blist[0][0])
    return bal

def login():
    uname=input("Enter your username:")
    pwd=input("Enter your password:")
    query="SELECT * from CUSTOMERS where CUSTOMER_USERNAME='%s' and CUSTOMER_PASSWORD='%s'" %(uname,pwd)
    con=getDBConnection()
    cur=con.cursor()
    cur.execute(query)
    clist=cur.fetchall()
    if len(clist)==0:
        return None
    else:
        return clist

def showPassbook(customerID):
    con=getDBConnection()
    cur = con.cursor()
    query = "SELECT ACCOUNT_NUMBER from ACCOUNTS where CUSTOMER_ID='%s'"%customerID
    cur.execute(query)
    aList = cur.fetchall()
    query="SELECT * from TRANSACTIONS where TRANSACTION_ID in\
          ( SELECT TRANSACTION_ID from TRANSACTIONS,ACCOUNTS\
          where (SENDER_ACCOUNT_NUMBER='%s' or RECEIVER_ACCOUNT_NUMBER='%s') and CUSTOMER_ID='%s')"%(aList[0][0],aList[0][0],customerID)

    cur.execute(query)
    tList = cur.fetchall()
    if len(tList)==0:
        return None
    else:
        return tList

def showMinistatement(customerID):
    tlist=showPassbook(customerID)
    if tlist is None:
        return None
    else:
        if len(tlist)<=10:
            txlist=tlist[-1::-1]
        else:
            txlist=tlist[-1:-11:-1]
        return txlist

    #print("TxnID\t\t  Type\t\tAmount\t\t\t  Timestamp\n----------------------------------------------------------------------------")
    #for txn in tlist:

def creditAmount(accountNumber,amt):
    con=getDBConnection()
    cur=con.cursor()
    curBalance=getAccountBalance(accountNumber)
    newBalance=amt+curBalance
    query="UPDATE ACCOUNTS SET ACCOUNT_BALANCE='%s' WHERE  ACCOUNT_NUMBER='%s'" %(str(newBalance),accountNumber)
    cur.execute(query)
    con.commit()

def debitAmount(accountNumber,amt):
    con=getDBConnection()
    cur=con.cursor()
    curBalance=getAccountBalance(accountNumber)
    newBalance=curBalance-amt
    query="UPDATE ACCOUNTS SET ACCOUNT_BALANCE='%s' WHERE  ACCOUNT_NUMBER='%s'" %(str(newBalance),accountNumber)
    cur.execute(query)
    con.commit()

def updateDetails(cRecord):
    con=getDBConnection()
    cur=con.cursor()
    query="UPDATE CUSTOMERS SET\
     CUSTOMER_NAME='%s',\
     CUSTOMER_PHONE='%s',\
     CUSTOMER_EMAIL='%s',\
     CUSTOMER_CITY='%s',\
     CUSTOMER_PASSWORD='%s'\
     WHERE CUSTOMER_ID='%s'"%(cRecord[1],cRecord[2],cRecord[3],cRecord[4],cRecord[5],cRecord[0])
    cur.execute(query)
    con.commit()
