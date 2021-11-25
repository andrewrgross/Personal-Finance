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
import matplotlib
import sys


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)
np.set_printoptions(edgeitems=3, infstr='inf',linewidth=200, nanstr='nan', precision=8,suppress=False, threshold=1000, formatter=None)


### 1 - Input

checkingA = pd.read_csv('C:/Users/grossar/Downloads/arg checking.csv')
savingsA  = pd.read_csv('C:/Users/grossar/Downloads/arg savings.csv')
checkingS = pd.read_csv('C:/Users/grossar/Downloads/mcgross checking.csv')
savingsS  = pd.read_csv('C:/Users/grossar/Downloads/mcgross savings.csv')

#creditA
#creditS

### 2 - Formatting
### 2.1 - Subset columns of interest
checkingA = checkingA.loc[:,['Effective Date','Amount','Balance','Transaction Category','Type','Extended Description']]
savingsA = savingsA.loc[:,['Effective Date','Amount','Balance','Transaction Category','Type','Extended Description']]
checkingS = checkingS.loc[:,['Effective Date','Amount','Balance','Transaction Category','Type','Extended Description']]
savingsS = savingsS.loc[:,['Effective Date','Amount','Balance','Transaction Category','Type','Extended Description']]

### 2.2 - Convert date strings to date objects
savingsA['Effective Date'] = pd.to_datetime(savingsA['Effective Date'], format = '%m/%d/%Y')
checkingA['Effective Date'] = pd.to_datetime(checkingA['Effective Date'], format = '%m/%d/%Y')
savingsS['Effective Date'] = pd.to_datetime(savingsS['Effective Date'], format = '%m/%d/%Y')
checkingS['Effective Date'] = pd.to_datetime(checkingS['Effective Date'], format = '%m/%d/%Y')

### 2.3 - Remove transactions of less than a dollar

def rmUnderDollar(dataframe):
    nRows = dataframe.shape[0]
    dataframe = dataframe.loc[abs(dataframe['Amount']) > 1]
    print('Removed ' + str(nRows - dataframe.shape[0]) + ' of ' + str(nRows) + ' rows')
    return(dataframe)

checkingA = rmUnderDollar(checkingA)
savingsA  = rmUnderDollar(savingsA)
checkingS = rmUnderDollar(checkingS)
savingsS  = rmUnderDollar(savingsS)

### 2.4 - Add week number

def addWeekNum(dataframe):
    weekList = []
    for rowNum in dataframe['Effective Date']:
        weekList.append(rowNum.isocalendar()[1])
    dataframe['Week'] = weekList
    return(dataframe)

checkingA = addWeekNum(checkingA)
savingsA  = addWeekNum(savingsA)
checkingS = addWeekNum(checkingS)
savingsS  = addWeekNum(savingsS)

### Summarize weeks
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