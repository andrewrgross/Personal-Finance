# -*- coding: utf-8 -*-
"""
Personal-Finance
Calculate distribution of monthly and weekly expenses
Created on Tue Nov 23 15:01:51 2021

@author: GrossAR
"""

### 0 - Header
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
import sys


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)
np.set_printoptions(edgeitems=3, infstr='inf',linewidth=200, nanstr='nan', precision=8,suppress=False, threshold=1000, formatter=None)


### 1 - Input
#os.chdir('C:/Users/grossar/Downloads/')
os.chdir('/home/andrew/Projects/Personal-Finance')

checkingA = pd.read_csv('arg checking.csv')
savingsA  = pd.read_csv('arg savings.csv')
checkingS = pd.read_csv('mcgross checking.csv')
savingsS  = pd.read_csv('mcgross savings.csv')
creditA   = pd.read_csv('creditA.csv')
creditS   = pd.read_csv('creditS-2020-21.csv')
investsS  = pd.read_csv('investmentsS1.csv')


### 2 - Formatting
### 2.1 - Subset columns of interest
checkingA = checkingA.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
savingsA  = savingsA.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
checkingS = checkingS.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
savingsS  = savingsS.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
creditA   = creditA.loc[:,['Date','Amount','Name']]
creditS   = creditS.loc[:,['Date','Amount','Description','Category','Card Member']]
investsS   = investsS.loc[:,['Trade Date', 'Net Amount', 'Transaction Description']]

### 2.2 - Rename columns
checkingA.columns = ['Date','Amount','Balance','Description','Type']
checkingS.columns = ['Date','Amount','Balance','Description','Type']
savingsA.columns = ['Date','Amount','Balance','Description','Type']
savingsS.columns = ['Date','Amount','Balance','Description','Type']
creditA.columns  = ['Date','Amount','Description']
creditS.columns  = ['Date','Amount','Description','Type','Card Member']
investsS.columns = ['Date','Amount','Description']

### 2.3 - Convert date strings to date objects
savingsA['Date']  = pd.to_datetime(savingsA['Date'], format = '%m/%d/%Y')
checkingA['Date'] = pd.to_datetime(checkingA['Date'], format = '%m/%d/%Y')
savingsS['Date']  = pd.to_datetime(savingsS['Date'], format = '%m/%d/%Y')
checkingS['Date'] = pd.to_datetime(checkingS['Date'], format = '%m/%d/%Y')
creditA['Date'] = pd.to_datetime(creditA['Date'], format = '%Y-%m-%d')
creditS['Date'] = pd.to_datetime(creditS['Date'], format = '%m/%d/%Y')
investsS['Date'] = pd.to_datetime(creditS['Date'], format = '%m/%d/%Y')

### 2.4 - Add Balance columns to credit
creditA.sort_values(by = 'Date', ascending = False, inplace = True)
creditS['Amount'] = np.array(creditS['Amount'])*-1

def addBalance(dataframe):
    balance = []
    newBalance = 0
    for amount in dataframe['Amount']:
        newBalance = newBalance - amount
        balance.append(newBalance)
    balance = np.around(np.array(balance) - max(balance), 2)
    dataframe['Balance'] = balance
    return(dataframe)

creditA = addBalance(creditA)
creditS = addBalance(creditS)

### 2.5 - Add Type column to USBank
creditA['Type'] = 'USBank_Purchase'
creditA['Type'].loc[creditA['Amount']>0] = 'BILL_PAYMENT'

### 2.5 - Add Card memeber to each
checkingA['Card Member'] = 'Andrew_checking'
savingsA['Card Member']  = 'Andrew_savings'
checkingS['Card Member'] = 'Shared_checking'
savingsS['Card Member']  = 'Shared_savings'
creditA['Card Member']   = 'Andrew_cc'

### 2.6 - Reorder Columns (again)
checkingA = checkingA.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'], copy = False)
checkingS = checkingS.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])
savingsA  = savingsA.reindex(columns = ['Date','Amount','Balance','Description','Type','Card Member'])
savingsS  = savingsS.reindex(columns = ['Date','Amount','Balance','Description','Type','Card Member'])
creditA  = creditA.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])
creditS  = creditS.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])


### 2.7 - Add week number

def addWeekNum(dataframe):
    weekList = []
    for rowNum in dataframe['Date']:
        weekList.append(rowNum.isocalendar()[1])
    dataframe['Week'] = weekList
    return(dataframe)

checkingA = addWeekNum(checkingA)
savingsA  = addWeekNum(savingsA)
checkingS = addWeekNum(checkingS)
savingsS  = addWeekNum(savingsS)
creditA   = addWeekNum(creditA)
creditS   = addWeekNum(creditS)

### 3.1 - plot

plt.plot(checkingA['Date'], checkingA['Balance'])
plt.plot(checkingS['Date'], checkingS['Balance'])
plt.plot(savingsA['Date'], savingsA['Balance'])
plt.plot(savingsS['Date'], savingsS['Balance'])

plt.plot(creditA['Date'], creditA['Balance'])
plt.plot(creditS['Date'], creditS['Balance'])



### 4.1 - Analyze
### Sum of inflow over a year
inflow = checkingA.loc[checkingA['Amount']>0]
cutoff = datetime(2020,11,27)
withinTimeRange = inflow['Date'] > cutoff
inflow = inflow.loc[withinTimeRange]
incomeAnum  = sum(inflow['Amount'])
incomeMonth = incomeAnum/12
incomeWeek  = incomeAnum/52

inflowS = checkingS.loc[checkingS['Amount']>0]
inflowS = inflowS.loc[inflowS['Date'] > datetime(2020,11,27)]
inflowS = inflowS.loc[inflowS['Type']!='Transfer']
test.reindex(inflowS)
test = inflowS.loc[i]

###Summarize weeks
dataframeSummary = pd.DataFrame(columns = ['Year', 'Week', 'Transactions', 'Inflow', 'Outflow', 'Min-Balance', 'Max-Balance'])


newRow = pd.DataFrame(columns = ['Year', 'Week', 'Transactions', 'Inflow', 'Outflow', 'Min-Balance', 'Max-Balance'])


for rowNum in range(0,dataframe.shape[0]):
    ### Identify the week of the current row
    weekCurrent = dataframe['Week'].iloc[rowNum]
    if 
    rowsWithSharedWeek = [rowNum]
    checking = True
    rowToCheck = rowNum
    while checking:
        rowToCheck = rowToCheck + 1
        if rowToCheck == dataframe.shape[0]:
            break
        if dataframe['Week'].iloc[rowToCheck] == weekCurrent:
            rowsWithSharedWeek.append(rowToCheck)
        else:
            checking = False
    dataCurrent = dataframe.iloc[rowsWithSharedWeek]
    ### For current data, analyze
    year = dataCurrent['Effective Date'].iloc[0].isocalendar()[0]
    week = dataCurrent['Effective Date'].iloc[0].isocalendar()[1]
    transactions = dataCurrent.shape[0]
    inflows  = dataCurrent['Amount'].loc[dataCurrent['Amount'] > 0]
    outflows = dataCurrent['Amount'].loc[dataCurrent['Amount'] < 0]
    inflow  = sum(inflows)
    outflow = sum(outflows)
    minBalance = min(dataCurrent['Balance'])
    maxBalance = max(dataCurrent['Balance'])
    newRow = pd.DataFrame(year, week, transactions, inflow, outflow, minBalance, maxBalance)

    newRow = pd.DataFrame({'Year' : [year], 'Week' : [week], 'Transactions' : [transactions], 'Inflow' : [inflow], 'Outflow' : [outflow], 'Min-Balance' : [minBalance], 'Max-Balance' : [maxBalance]})
    dataframeSummary = pd.concat([dataframeSummary,newRow], ignore_index = True, axis = 0)
    


### 3 - Analysis

### For each week, determine the min, max, and number of withdrawls and deposits
### Identify the range covered in the data
dateStart = 
### Create a data frame with a row for each week

### 4 - Plotting



### 5 - Output