#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlalchemy as db
from sqlalchemy import exc
import sys
import logging

from manager import manager #importing manager class 



class Bank(manager):
    """
    Bank is a banking application that takes the following inputs:
    1. Create Banking Account
    2. Deposit Amount
    3. Withdraw Amount
    4. Check Account status
    5. Close Account
    6. Close Application
    """

    def __init__(self):
        manager.__init__(self)
        self.main()
        
    #function to create a new account
    def create_acc(self):
        
        try:

            self.first_name = input("Enter the account holder first name : \n")
            self.last_name = input("Enter the account holder last name : \n")
            self.dob = int(input("Enter the account holder date of birth : \n"))
            self.email = input("Enter the account holder email: \n")
            self.acc_type = input("Account type (saving/checking): \n")
            self.balance = int(input("Enter opening balance: \n"))
            
    
    
            query = db.insert(self.Customer).values(first_name=self.first_name, last_name=self.last_name, dob=self.dob,
                                               status='Active', email=self.email, acc_type=self.acc_type,
                                               balance=self.balance)
    
            ResultProxy = self.execute(query)
            query1 = db.select([self.Customer])
            results = self.fetchall(query1)
            print(results)
    
            print('\n  New customer added successfully!\n\n')
        except ValueError:
            
            print( "\n********\nInvalid input!\n*********\n TypeError. Please try again!\n")

            self.logger.error("Type Error. Invalid input in create_acc()")
            self.main()
            
 
    #function to deposit money in an account
    def deposit(self):

        self.acc_no = input('Enter your account number: \n')
        self.amount = input('Enter the amount to deposit: \n')
        

        result = self.check_status(self.acc_no)

        try:
            self.amount = int(self.amount)
            if result[0] == 'Active':

                query = self.Customer.update().values(balance=self.amount+self.Customer.columns.balance)\
                    .where(db.and_(self.Customer.columns.acc_no == self.acc_no, self.Customer.columns.status == 'Active'))
    
                ResultProxy = self.execute(query)
                query1 = db.select([self.Customer])
                results = self.fetchall(query1)
                print(results)
    
                print('\n  Deposited successfully!\n\n')
            else:

                self.logger.error("ValueError. Invalid input for the account number: '{}' in close(). Account is closed. in deposit()".format(self.acc_no))
                print("\n*******\nInvalid input!\n*********\n ValueError. The account is already closed. Please try again!\n")
                self.main()
        
           
            self.main()
        except TypeError:
            print( "\n********\nInvalid input!\n*********\n TypeError. Please try again!\n")

            self.logger.error("Type Error. Invalid input: with the account number:'{}'.in close()".format(self.acc_no))
            
        except ValueError:
            
            print( "\n********\nInvalid input!\n*********\n ValueError with amount. Please try again!\n")

            self.logger.error("Value Error. Invalid input: with the account :'{}'.in close()".format(self.acc_no))

    #function to withdraw money from account
    def withdraw(self):

        try:

            self.acc_no = input('Enter your account number: ')
            self.amount = input('Enter the amount to withdraw: ')
            self.amount = int(self.amount)
            result = self.check_status(self.acc_no)

            if result[0] == 'Active':

                query = self.Customer.update().values(balance=self.Customer.columns.balance-self.amount)\
                    .where(db.and_(self.Customer.columns.acc_no == self.acc_no, self.Customer.columns.status == 'Active'))
            
                ResultProxy = self.execute(query)
                query1 = db.select([self.Customer])
                results = self.fetchall(query1)
                print(results)

                print('\n   Withdrawl conducted successfully!\n\n')

            else:
                self.logger.error("ValueError. Invalid input for the account number: '{}' in withdraw(). Account is closed. in deposit()".format(self.acc_no))
                print("\n*******\nInvalid input!\n*********\n ValueError. The account is already closed. Please try again!\n")
                self.main()
        
        except TypeError:
            print( "\n********\nInvalid input!\n*********\n TypeError. Please try again!\n")

            self.logger.error("Type Error. Invalid input: with the account number:'{}'.in withdraw()".format(self.acc_no))
            
        except ValueError:
            
            print( "\n********\nInvalid input!\n*********\n ValueError with amount. Please try again!\n")

            self.logger.error("Value Error. Invalid input: with the amount :'{}'.in withdraw()".format(self.acc_no))

    #function to close an account
    def close(self):
        
        
        self.acc_no = input('Enter the account number of the account to be closed: ')
        result = self.check_status(self.acc_no)
        
        try:
            
            if result[0] == 'Active':
    
                query = self.Customer.update().values(status='Inactive')\
                    .where(db.and_(self.Customer.columns.acc_no == self.acc_no, self.Customer.columns.status == 'Active'))
        
                ResultProxy = self.execute(query)
                query1 = db.select([self.Customer])
                results = self.fetchall(query1)
                print(results)
                print(ResultProxy)
                print('Account closed successfully!\n\n')
            
            else:
                self.logger.error("ValueError. Invalid input for the account number: '{}' in close(). Account is already closed".format(self.acc_no))
                print("\n*******\nInvalid input!\n*********\n ValueError. The account is already closed. Please try again!\n")
                self.main()
            
        except TypeError:
            
            self.logger.error("TypeError. Invalid input for the account number: '{}' in close().".format(self.acc_no))
            print("\n*******\nInvalid input!\n*********\n TypeError. Please try again!\n")
            
            
        
    #function to close the main menu
    def closeall(self):
        print('\n  Thank you for using the Bank')
        sys.exit(0)

    #function to check account status (active/inactive)
    def check_status(self, acc_no):

        try:

            query = db.select([self.Customer.columns.status]).where(
                self.Customer.columns.acc_no == acc_no)

            p = self.fetchone(query)
            print('\n  The account is {}'.format(p[0]))
            return p

        except TypeError as err:
            print(
                "\n********\nInvalid input!\n*********\n TypeError. Please try again!\n")

            self.logger.error(
                "Type Error. Invalid input: with the account number:'{}'.in check_status()".format(acc_no))


    #function to take interact with the user
    def main(self):

        while True:

            print("\n----- MAIN MENU ----- ")
            print("\n1.  Create Account")
            print("\n2.  Deposit")
            print('\n3.  Withdrawl')
            print('\n4.  Check account status')
            print('\n5.  Close account')
            print('\n6.  Close application')
            print('\n\n')

            option = input('Enter your option: ')

            #calling different functions based on user's input
            if option == '1':
                self.create_acc()
            elif option == '2':
                self.deposit()
            elif option == '3':
                self.withdraw()
            elif option == '4':
                n = input('Enter the account number: ')
                o = self.check_status(n)
            elif option == '5':
                self.close()
            elif option == '6':
                self.closeall()
            else:
                self.logger.error( "Type Error. Invalid input in main()")
                print('\nWrong option, try again')



Bank()