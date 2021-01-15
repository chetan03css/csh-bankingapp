import bankAPI

def showPassbook(customerID):
    con=bankAPI.getDBConnection()
    cur = con.cursor()
    query = "select ACCOUNT_NUMBER from accounts where customer_id='%s'"%customerID
    cur.execute(query)
    aList = cur.fetchall()
    query="select * from transactions where transaction_id in\
          ( select transaction_id from transactions,accounts\
          where (sender_account_number='%s' or RECEIVER_ACCOUNT_NUMBER='%s') and customer_id='%s')"%(aList[0][0],aList[0][0],customerID)
    
    cur.execute(query)
    tList = cur.fetchall()
    #print(tList)
    print("Passbook Till Date\n----------------------------")
    print("TxnID\t\t  Type\t\tAmount\t\t\t  Timestamp\n----------------------------------------------------------------------------")
    tType = ""
    
    for x in tList:
        if aList[0][0] == x[1]:
            tType = "DEBIT"
        elif aList[0][0] == x[2]:
            tType = "CREDIT"
            
        print(x[0],"\t",tType,"   \tINR ",x[3],"/-\t",x[4])
    

showPassbook('ACB1000001')

