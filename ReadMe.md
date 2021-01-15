NetBanking app using python mysql

Project: CSH BANK APP

Use Case : NETBANKING APPLICATION

Functional Requirement Specifications:
---------------------------------------

Need : Net Banking Application 

Functions:

1. Customer Login 
2. Customer Profile & Account Opening
3. UPI ID Generation
4. Customer Account Closing
5. NetBanking Services
		 i. Pass Book 
		ii. Mini Statement 
	   	iii. Money Transfer 
		iv. Update Customer Details 

Database Design:
-----------------

1. The Bank Application interacts with a database which maintains following tables :

	bankdb : tables 

The tables contain respective data. 
	
			 1. CUSTOMERS : CustomerID, Name, Phone, EMail ID, Address, UPI ID, Username, Password 
			 2. ACCOUNTS : CustomerID, ACCOUNT_NUMBER, ACCOUNT_TYPE, ACCOUNT_BALANCE, ACCOUNT_STATUS
			 3. TRANSACTIONS: TRANSACTION_ID, SENDER_ACCOUNT_NUMBER, RECEIVER_ACCOUNT_NUMBER,
						      AMOUNT, TXN_TIMESTAMP, TXN_STATUS
			 
2. CustomerID : 10 digit alphanumeric ID 
				Ex: "ACB1000001", "ACB1000002" ...
			
				
   ACCOUNT_NUMBER : 10 digit account number 
					Ex: 1000000000, 1000000001, 1000000002.......9882345661 .. 
					
	TRANSACTIONS : 10 digit transaction id 
					Ex: TR10000001, TR10000002 ... 
					
	UPI_ID : phone_number@upibank 
			ex: 9035111111@okaxis, 9035111122@okhdfc, 9035444111@ybl
		
	user_name : emailID_username
				

note : ALL THESE VALUES should be AUTO-INCREMENTED/AUTO_GENERATED.

3. Banking APIs 
-----------------

Module : bankAPI.py 


getDBConnection() : connects to DB and returns the connection object

openNewBankAccount() : opens new bank account 

closeBankAccount(accountNumber) : Makes the ACCOUNT_STATUS of given accountNumber as "CLOSED"

validateAccountNumber(accountNumber) : returns True if accountNumber exists else False

getAccountNumber(customerID) : returns accountNumber of given customerID

getAccountBalance(accountNumber) : returns balance of given accountNumber

login() : validates username password and opens a netbanking session, exits with error if failed.

showPassbook(customerID) : returns transaction details of particular customerID

showMinistatement(customerID) : latest 10 transactions of customerID

creditAmount(accountNumber,amt) : credits accountNumber with given amount 

debitAmount(accountNumber,amt) : debits accountNumber with given amount 

updateDetails(cRecord) : updates fields in user account.
			 
			 
4. Banking Client :

		 Filename : bankApplication.py 

MAIN MENU
----------

1. Open A New Bank Account
2. Close Your Bank Account
3. NetBanking Services

	1.Passbook
	2.Mini Statement
	3.Transfer Money
	4.Check Balance
	5.Update Details
	6.Logout
	
4. Exit		 

Respective APIs should be consumed/called. 


----------------------------------------------

5. DATABASE LOCATIONS

	CENTRAL : AWS EC2 Ubuntu Server with MySQL DB
