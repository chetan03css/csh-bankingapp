from os import system
from time import sleep
from bankAPI import *

x = "-" * 33
y = "|      Welcome to City Bank\t|"
z = "-" * 26

optionValue = 1
while optionValue:
    system("cls")
    print(x)
    print(y)
    print(x)
    print("\n\tMAIN MENU")
    print(z)

    print("1. Open A New Bank Account")
    print("2. Close Your Bank Account")
    print("3. NetBanking Services")
    print("4. Exit\n")

    optionValue = int(input("Choose your options to proceed:  "))

    if optionValue == 1:
        print()
        system('cls')
        openNewBankAccount()
        input("Press Enter to close.")

        # print("option ",optionValue)
        # call the Open new account function

    elif optionValue == 2:
        accNumber = input("Enter Account Number to Close:")
        closeBankAccount(accNumber)
        input("Press Enter to close.")
        # print("option ", optionValue)
        # call close account function
    elif optionValue == 3:
        #print("NET BANKING APIs, Option  ", optionValue)
        clist=login()
        #print(clist)
        system('cls')

        if clist is not None:
            print("Hi ",clist[0][1]," Welcome to City Bank")
            nFlag=1
            while nFlag:

                print("\n\n1.Passbook\n2.Mini Statement\n3.Transfer Money\n4.Check Balance\n5.Update Details\n6.Logout")
                opt=int(input("Please choose your options:"))
                if opt==1:

                    tList = showPassbook(clist[0][0])
                    aList = getAccountNumber(clist[0][0])

                    system('cls')
                    if tList is not None:
                        print("Passbook Till Date\n----------------------------")
                        print("TxnID\t\t  Type\t\t    Amount\t\t   Date\t     Time\n----------------------------------------------------------------------------")
                        tType = ""

                        for txns in tList:
                            if aList == txns[1]:
                                tType = "DEBIT"
                            elif aList == txns[2]:
                                tType = "CREDIT"

                            print(txns[0],"\t",tType,"   \tINR ",txns[3],"/-\t\t",txns[4])
                    else:
                        print("No Transactions Yet\n")

                elif opt==2:
                    tlist=showMinistatement(clist[0][0])
                    alist=getAccountNumber(clist[0][0])

                    system('cls')
                    if tlist is not None:
                        print("Mini Statement\n-------------------")
                        print("Sr. No.\tTxnID\t\t  Type\t\t    Amount\t\t   Date\t     Time\n-------------------------------------------------------------------------------------")
                        tType = ""
                        i=1
                        for txns in tlist:
                            if alist== txns[1]:
                                tType = "DEBIT"
                            elif alist== txns[2]:
                                tType = "CREDIT"

                            print(" ",i,")  ",txns[0],"\t",tType,"   \tINR ",txns[3],"/-\t\t",txns[4])
                            i=i+1

                    else:
                        print("\nNo Transactions Yet\n")


                elif opt==3:
                    system('cls')
                    print("WELCOME TO NET BANKING PORTAL")
                    print(x)
                    con=getDBConnection()
                    cur=con.cursor()

                    sender=getAccountNumber(clist[0][0])

                    receiver=input("Enter Recipient Account Number: ")
                    if validateAccountNumber(receiver):
                        curBalance=getAccountBalance(sender)
                        damount=int(input("Enter the amount to Deposit: "))
                        if damount > curBalance:
                            print("Transaction Failed! Insufficient Funds")
                        else:
                            debitAmount(sender,damount)
                            creditAmount(receiver,damount)
                            query="INSERT INTO TRANSACTIONS\
                            (TRANSACTION_ID,SENDER_ACCOUNT_NUMBER,RECEIVER_ACCOUNT_NUMBER,AMOUNT,TXN_STATUS)\
                             VALUES(%s,%s,%s,%s,%s)"
                            cur.execute("SELECT TRANSACTION_ID FROM TRANSACTIONS")
                            tlist=cur.fetchall()

                            if len(tlist)==0:
                                tid = 'TR10000000'
                            else:
                                tid = tlist[-1][0]

                            txnid = int(tid[2::1])
                            txnid = txnid + 1
                            txnid = "TR" + str(txnid)
                            txnlist=[(txnid,sender,receiver,damount,"SUCCESS")]
                            cur.executemany(query,txnlist)
                            con.commit()
                            cur.execute("SELECT * FROM TRANSACTIONS WHERE TRANSACTION_ID='%s'"%txnid)
                            tlist=cur.fetchall()
                            if len(tlist)!=0:

                                print("\nPayment Successful!")
                                print("Transaction ID:",txnid)
                                print("Pais Rs ",damount,"/-")
                                #use case to display recipient name also, take as a Change Request From Client
                                print("Date and Time:",tlist[-1][-2])
                                print("Available Balance: Rs ",getAccountBalance(sender),"/-")
                            else:
                                print("Payment Failed")
                    else:
                        print("Invalid Recipient Account Number!")

                elif opt==4:
                    print("\nAvailable Balance = Rs",getAccountBalance(getAccountNumber(clist[0][0])),"/-")

                elif opt==5:
                    print("Update Details Portal\n------------------------")
                    print("Hi",clist[0][1],", only the below details can be changed.")
                    oFlag=1
                    print("To Update : Choose the option you want to update.")
                    print("To Submit All the changes, press 6.\n")
                    updatedList = [clist[0][0],clist[0][1],clist[0][2],clist[0][3],clist[0][4],clist[0][6]]
                    while oFlag:
                        print("\n1.Name\n2.Phone Number\n3.Email ID\n4.Current City\n5.Password\n6.Close")
                        updateOpt=int(input("Please Choose any option 1-5 to update your details\nChoose 6 to close this window."))
                        if updateOpt==1:
                            updatedList[1]=input("Enter Your Name : ")
                        elif updateOpt==2:
                            updatedList[2]=input("Enter Your New Phone Number : ")
                        elif updateOpt==3:
                            updatedList[3]=input("Enter Your New Email ID : ")
                        elif updateOpt==4:
                            updatedList[4]=input("Enter Your Current City : ")
                        elif updateOpt==5:
                            updatedList[5]=input("Enter new password : ")
                        elif updateOpt==6:
                            oFlag=0
                        else:
                            print("Invalid Option, Choose 1-6 only.")

                    updateDetails(updatedList)
                    print("Details Updated Successfully!")

                elif opt==6:
                    nFlag=0


                else:
                    print("Invalid Option! Please choose between 1-5")
        else:
            print("Username or Password is Invalid!Please try again")

        input("Press Enter to close.")
        # call net banking APIs

    elif optionValue == 4:
        print("\n\nThanks for using City Bank.")
        input("Press Enter to close.")
        optionValue = 0
    else:
        print("\nINVALID OPTION.\nPLEASE CHOOSE AN OPTION BETWEEN 1-5 ONLY.\nTRY AGAIN")
        input("Press Enter to Try Again.")

print("APP CLOSED.")
