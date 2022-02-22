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
import datetime
#from datetime import datetime  # is this necessary?
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import math
import os
import sys


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)
np.set_printoptions(edgeitems=3, infstr='inf',linewidth=200, nanstr='nan', precision=8,suppress=False, threshold=1000, formatter=None)

### 0.2 - Functions

def addBalance(dataframe):
    balance = []
    newBalance = 0
    for amount in dataframe['Amount']:
        newBalance = newBalance - amount
        balance.append(newBalance)
    balance = np.around(np.array(balance) - max(balance), 2)
    dataframe['Balance'] = balance
    return(dataframe)

def rmUnderDollar(dataframe):
    nRows = dataframe.shape[0]
    dataframe = dataframe.loc[abs(dataframe['Amount']) > 1]
    print('Removed ' + str(nRows - dataframe.shape[0]) + ' of ' + str(nRows) + ' rows')
    return(dataframe)

def addWeekNum(dataframe):
    weekList = []
    for rowNum in dataframe['Date']:
        weekList.append(rowNum.isocalendar()[1])
    dataframe['Week'] = weekList
    return(dataframe)

def addWeeksAgo(dataframe):
    today = datetime.datetime.today()
    lastSun = today - datetime.timedelta(today.weekday() +1 %7)
    weekList = []
    for rowNum in dataframe['Date']:
        weeksAgo = math.floor((lastSun - rowNum).days/7)
        weekList.append(weeksAgo)
    dataframe['WeeksAgo'] = weekList
    return(dataframe)
        
def summarizeWeeks(dataframe, balanceFinal):
    today = datetime.datetime.today()
    dataframeSummary = pd.DataFrame(columns = ['Date', 'WeeksAgo', 'balanceStart', 'balanceFinal','nOutflow', 'totalOutflow', 'nInflow', 'totalInflow', 'transactions', 'Amount'])
    weekRange = range(min(dataframe['WeeksAgo']), max(dataframe['WeeksAgo'] + 1))
    balanceStart = balanceFinal
    for week in weekRange:
        date = (today - datetime.timedelta(weeks = week)).date() #.strftime("%b %d %Y")
        #balanceStart = balanceFinal
        balanceFinal = balanceStart
        #print('Week: ' + str(week))
        rowsSelected = dataframe['WeeksAgo'] == week
        subset = dataframe.loc[rowsSelected]
        if len(subset) == 0:
            newRow = pd.DataFrame({'Date': [date], 'WeeksAgo': [week], 'balanceStart': [balanceStart], 'balanceFinal': [balanceFinal],'nOutflow': [0], 'totalOutflow': [0], 'nInflow': [0], 'totalInflow': [0], 'transactions': [0], 'Amount': [0]})
        else:
            ### Save key stats:
            outflows = subset.loc[subset['Amount'] <0]['Amount']
            totalOutflow = sum(outflows)
            nOutflow = len(outflows)
            
            inflows  = subset.loc[subset['Amount'] >0]['Amount']
            totalInflow = sum(inflows)
            nInflow = len(inflows)
        
            transactions = len(subset)
            change = sum(subset['Amount'])
            #balanceFinal = balanceStart + change
            balanceStart = balanceFinal - change
            newRow = pd.DataFrame({'Date': [date], 'WeeksAgo': [week], 'balanceStart': [balanceStart], 'balanceFinal': [balanceFinal],'nOutflow': [nOutflow], 'totalOutflow': [totalOutflow], 'nInflow': [nInflow], 'totalInflow': [totalInflow], 'transactions': [transactions], 'Amount': [change]})
    
        dataframeSummary = pd.concat([dataframeSummary,newRow], ignore_index = True, axis = 0)

    #startingBalance = -dataframeSummary['balanceFinal'][0]
    return(dataframeSummary)

### 1 - Input
#os.chdir('C:/Users/grossar/Downloads/')
os.chdir('/home/andrew/Projects/Personal-Finance')

checkingA = pd.read_csv('arg checking.csv')
savingsA  = pd.read_csv('arg savings.csv')
checkingS = pd.read_csv('mcgross checking.csv')
savingsS  = pd.read_csv('mcgross savings.csv')
creditA   = pd.read_csv('creditA.csv')
creditS   = pd.read_csv('creditS.csv')
investVan  = pd.read_csv('investVan.csv', header = 3)

### 2 - Formatting

# Assign transfers to Type

checkingS['Card Member'] = ''
checkingS['Type'].loc[checkingS['Transaction Category'] == 'Transfer'] = 'Transfer'

### 2.1 - Subset columns of interest
checkingA = checkingA.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
savingsA  = savingsA.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
checkingS = checkingS.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
savingsS  = savingsS.loc[:,['Effective Date','Amount','Balance', 'Description','Type']]
creditA   = creditA.loc[:,['Date','Amount','Name']]
creditS   = creditS.loc[:,['Date','Amount','Description','Category','Card Member']]
investVan   = investVan.loc[:,['Trade Date', 'Net Amount', 'Transaction Description', 'Transaction Type']]

### 2.2 - Rename columns
checkingA.columns = ['Date','Amount','Balance','Description','Type']
checkingS.columns = ['Date','Amount','Balance','Description','Type']
savingsA.columns = ['Date','Amount','Balance','Description','Type']
savingsS.columns = ['Date','Amount','Balance','Description','Type']
creditA.columns  = ['Date','Amount','Description']
creditS.columns  = ['Date','Amount','Description','Type','Card Member']
investVan.columns = ['Date','Amount','Description', 'Type']

### 2.3 - Convert date strings to date objects
savingsA['Date']  = pd.to_datetime(savingsA['Date'], format = '%m/%d/%Y')
checkingA['Date'] = pd.to_datetime(checkingA['Date'], format = '%m/%d/%Y')
savingsS['Date']  = pd.to_datetime(savingsS['Date'], format = '%m/%d/%Y')
checkingS['Date'] = pd.to_datetime(checkingS['Date'], format = '%m/%d/%Y')
creditA['Date'] = pd.to_datetime(creditA['Date'], format = '%Y-%m-%d')
creditS['Date'] = pd.to_datetime(creditS['Date'], format = '%m/%d/%Y')
investVan['Date'] = pd.to_datetime(investVan['Date'], format = '%m/%d/%Y')

### 2.4 - Add Balance columns
###### to credit
creditA.sort_values(by = 'Date', ascending = False, inplace = True)
creditS['Amount'] = np.array(creditS['Amount'])*-1

creditA = addBalance(creditA)
creditS = addBalance(creditS)

###### to investment
typeCol = np.array(investVan['Type'])
rowsToKeep = np.array(typeCol != 'Buy') * np.array(typeCol != 'Sweep in') * np.array(typeCol != 'Sweep out') * np.array(typeCol != 'Reinvestment') * np.array(typeCol != 'Reinvestment (LT gain)') * np.array(typeCol != 'Reinvestment (ST gain)') 
investVan  = investVan.loc[rowsToKeep]
balance = []
newBalance = 0
for amount in np.flip(investVan['Amount']):
    newBalance = round(newBalance + amount, 2)
    balance.append(newBalance)

investVan['Balance'] = np.flip(balance)

### 2.5 - Add Type column to USBank
creditA['Type'] = 'USBank_Purchase'
creditA['Type'].loc[creditA['Amount']>0] = 'BILL_PAYMENT'
transferList = []
for entry in savingsS['Description']:
    transferList.append('Transfer' in entry)


### 2.5 - Add Card memeber to each
checkingA['Card Member'] = 'Andrew_checking'
savingsA['Card Member']  = 'Andrew_savings'
checkingS['Card Member'] = 'Shared_checking'
savingsS['Card Member']  = 'Shared_savings'
creditA['Card Member']   = 'Andrew_cc'
investVan['CardMember']  = 'Vanguard'

### 2.6 - Reorder Columns (again)
checkingA = checkingA.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'], copy = False)
checkingS = checkingS.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])
savingsA  = savingsA.reindex(columns = ['Date','Amount','Balance','Description','Type','Card Member'])
savingsS  = savingsS.reindex(columns = ['Date','Amount','Balance','Description','Type','Card Member'])
creditA  = creditA.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])
creditS  = creditS.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])
investVan= investVan.reindex(columns= ['Date','Amount','Balance','Description','Type','Card Member'])

### 2.7 - Remove transactions of less than a dollar

checkingA = rmUnderDollar(checkingA)
savingsA  = rmUnderDollar(savingsA)
checkingS = rmUnderDollar(checkingS)
savingsS  = rmUnderDollar(savingsS)

### 2.8 - Add week number

checkingA = addWeeksAgo(checkingA)
savingsA  = addWeeksAgo(savingsA)
checkingS = addWeeksAgo(checkingS)
savingsS  = addWeeksAgo(savingsS)
creditA   = addWeeksAgo(creditA)
creditS   = addWeeksAgo(creditS)
investVan = addWeeksAgo(investVan)

### 2.9 - Trim all to same start

checkingA = checkingA.loc[checkingA['Date'] > datetime.datetime(2021, 1, 1, 1, 1)]
checkingS = checkingS.loc[checkingS['Date'] > datetime.datetime(2021, 1, 1, 1, 1)]
savingsA  = savingsA.loc[savingsA['Date']   > datetime.datetime(2021, 1, 1, 1, 1)]
savingsS  = savingsS.loc[savingsS['Date']   > datetime.datetime(2021, 1, 1, 1, 1)]
creditA   = creditA.loc[creditA['Date']     > datetime.datetime(2021, 1, 1, 1, 1)]
creditS   = creditS.loc[creditS['Date']     > datetime.datetime(2021, 1, 1, 1, 1)]
investVan = investVan.loc[creditS['Date']     > datetime.datetime(2021, 1, 1, 1, 1)]

### 2.10 - Add a point for the current time


### 2.10 - Remove the transfer to investment
#checkingA.loc[checkingA['Amount'] == -3000]
#investmentRow = 103
#checkingA['Balance'].iloc[0:investmentRow] = checkingA['Balance'].iloc[0:investmentRow] + 3000

####### 3 - Plot
### 3.1 - plot

####### 4 - Analyze changes over time
### 4.1 - Find the balance for each source
balChecking = checkingA['Balance'].iloc[0] + checkingS['Balance'].iloc[0]
balSavings  = savingsA['Balance'].iloc[0]  + savingsS['Balance'].iloc[0]
balCredit   = creditA['Balance'].iloc[0]   + creditS['Balance'].iloc[0]
balInvest   = investVan['Balance'].iloc[0]
balTotal    = balChecking  +  balSavings  +  balCredit + balInvest

print('Checking Balance: $' + str(balChecking))
print('Savings Balance: $' + str(balSavings))
print('Credit Balance: $' + str(balCredit))
print('Investments Balance: $' + str(balInvest))
print('TOTAL ACCOUNTS BALANCE: $' + str(balTotal))


### 4.2 - Join ledgers
checking = pd.concat([checkingA, checkingS], ignore_index = True, axis = 0)
checking = checking.sort_values(['Date'], ascending = False)
summaryChecking = summarizeWeeks(checking, balanceFinal = balChecking)

savings = pd.concat([savingsA, savingsS], ignore_index = True, axis = 0)
savings = savings.sort_values(['Date'], ascending = False)
summarySav = summarizeWeeks(savings, balanceFinal = balSavings)

credit = pd.concat([creditA, creditS], ignore_index = True, axis = 0)
credit = credit.sort_values(['Date'], ascending = False)
summaryCredit = summarizeWeeks(credit, balanceFinal = balCredit)

invest = investVan
summaryInvest = summarizeWeeks(invest, balanceFinal = balInvest)

allAccts = pd.concat([checking, savings, credit, invest], ignore_index = True, axis = 0)
allAccts = allAccts.sort_values(['Date'], ascending = False)
summaryAll = summarizeWeeks(allAccts, balanceFinal = balTotal)

### 4.3 - Isolate inflow and outflows by source
####### 4.3.1 - Isolate Amex payments from shared

checkingAb = checkingA.loc[checkingA['Type']!='Transfer']
checkingSb = checkingS.loc[checkingS['Type']!='Transfer']
amex = []
for row in checkingSb['Description']:
    amex.append('AMEX EPAYMENT' in row)
checkingSb['Amex'] = amex

summaryCheckingA = summarizeWeeks(checkingAb, balanceFinal = checkingAb['Balance'].iloc[0])
summaryCheckingS = summarizeWeeks(checkingSb, balanceFinal = checkingS['Balance'].iloc[0])
summaryCreditA   = summarizeWeeks(creditA, balanceFinal = creditA['Balance'].iloc[0])
summaryCreditS   = summarizeWeeks(creditS, balanceFinal = creditS['Balance'].iloc[0])
summaryInOut = pd.concat([summaryCreditS['WeeksAgo'], summaryCheckingA['totalInflow'], summaryCheckingA['totalInflow']+summaryCheckingS['totalInflow'], summaryCreditA['totalOutflow'], summaryCreditA['totalOutflow'] + summaryCreditS['totalOutflow']], axis = 1)
summaryInOut.columns = ['WeeksAgo', 'incomeA', 'incomeS', 'spendingA', 'spendingS']
summaryInOut['difference'] = summaryInOut['incomeS'] + summaryInOut['spendingS']

### 4.4 - Plots
###### 4.4.1 - Plot balance total over time
fig, ax = plt.subplots(figsize = (12, 8))
ax.plot(summaryInvest['Date'], summaryInvest['balanceFinal'], label = 'Investments', color = 'wheat')
ax.plot(summarySav['Date'], summarySav['balanceFinal'], label = 'Savings', color = 'lightgreen')
ax.plot(summaryCredit['Date'], summaryCredit['balanceFinal'], label = 'Credit', color = 'salmon')
#ax.plot(checkingA['Date'], checkingA['Balance'], label = 'Checking, Andy', color = 'mediumorchid')
#ax.plot(checkingS['Date'], checkingS['Balance'], label = 'Checking, Shared', color = 'blue')
ax.plot(summaryChecking['Date'], summaryChecking['balanceFinal'], label = 'Checking', color = 'blue')
ax.plot(summaryAll['Date'], summaryAll['balanceFinal'], label = 'All', color = 'navy', linewidth = 4)
plt.axhline(y = 0, color = 'black', linewidth = 1)
ax.set_xlabel('Date',  fontsize = 16)
ax.set_ylabel('Dollars', fontsize = 16)
ax.set_title('Balance over time', fontsize = 20)
plt.xticks(fontsize= 11, rotation = -45)
ax.yaxis.grid()
ax.xaxis.grid()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.yaxis.set_major_locator(mtick.LinearLocator(numticks = 14))
ax.yaxis.set_major_locator(plt.MaxNLocator(12))
ax.legend(loc=2, prop={'size': 12})
plt.xlim([datetime.date(2021, 1, 1),datetime.datetime.now()])
plt.ylim([-6000,20000])
plt.show()


###### 4.4.2 - Plot recent weeks

fig, ax = plt.subplots(figsize = (12, 8))

weeksAgo = summaryInOut['WeeksAgo'][0:10]
incomeA = summaryInOut['incomeA'][0:10]
incomeS = summaryInOut['incomeS'][0:10]
spendingA = summaryInOut['spendingA'][0:10]
spendingS = summaryInOut['spendingS'][0:10]
difference = summaryInOut['difference'][0:10]

ax.bar(weeksAgo,incomeS, color = 'cornflowerblue')
ax.bar(weeksAgo,incomeA, color = 'mediumblue')
ax.bar(weeksAgo,spendingS, color = 'firebrick')
ax.bar(weeksAgo, spendingA, color = 'salmon')
plt.axhline(y = 0, color = 'black', linewidth = 1)
plt.scatter(weeksAgo,difference, color = 'orange', s = 150, zorder = 9)
for i, label in enumerate(incomeS):
    plt.text(weeksAgo[i], (incomeS[i]+100), "$"+str(round(label)), size = 14, ha = 'center')

for i, label in enumerate(spendingS):
    plt.text(weeksAgo[i], (spendingS[i]-300), "$"+str(round(abs(label))), size = 14, ha = 'center')
    
#ax.legend(['First line', 'Second line'])
#colors = {'fruit':'red', 'veggie':'green'}         
#labels = list(colors.keys())
#handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
#plt.legend(handles, labels)

ax.set_xlabel('Weeks Ago',  fontsize = 16)
ax.set_ylabel('Dollars', fontsize = 16)
ax.set_title('Cashflow', fontsize = 20)
plt.xlim([9,-2])
plt.show()










# find the range of weeks for a dataframe


summaryCheckA = summarizeWeeks(checkingA, checkingA['Balance'].iloc[0])
summaryCheckS = summarizeWeeks(checkingS, checkingS['Balance'].iloc[0])
summarySavA   = summarizeWeeks(savingsA,  savingsA['Balance'].iloc[0])
summarySavS   = summarizeWeeks(savingsS,  savingsS['Balance'].iloc[0])
summaryCCA    = summarizeWeeks(creditA,   creditA['Balance'].iloc[0])
summaryCCS    = summarizeWeeks(creditS,   creditS['Balance'].iloc[0])


### 4.1.1 - Test summarization with plot
fig, ax = plt.subplots()
ax.plot(summaryCheckA['WeeksAgo'], summaryCheckA['balanceFinal'], label = 'Checking, Personal')
ax.plot(summaryCheckS['WeeksAgo'], summaryCheckS['balanceFinal'], label = 'Checking, Shared')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
plt.xlim([104,0])
ax.legend()
plt.show()

### 4.2.1 - Join checking summaries
checking = pd.concat([checkingA, checkingS], ignore_index = True, axis = 0)
checking = checking.sort_values(['Date'], ascending = False)
checkingSum = checkingA['Balance'].iloc[0] + checkingS['Balance'].iloc[0]
summaryChecking = summarizeWeeks(checking, balanceFinal = checkingSum)
### 4.2.2 - Plot joined checking summaries
fig, ax = plt.subplots()
ax.plot(summaryCheckA['WeeksAgo'], summaryCheckA['balanceFinal'], label = 'Checking, Personal')
ax.plot(summaryCheckS['WeeksAgo'], summaryCheckS['balanceFinal'], label = 'Checking, Shared')
ax.plot(summaryChecking['WeeksAgo'], summaryChecking['balanceFinal'], label = 'Checking, All')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
plt.xlim([104,0])
ax.legend()
plt.show()

### 4.2.3 - Join savings summaries
savings = pd.concat([savingsA, savingsS], ignore_index = True, axis = 0)
savings = savings.sort_values(['Date'], ascending = False)
savingsSum = savingsA['Balance'].iloc[0] + savingsS['Balance'].iloc[0]
summarySav = summarizeWeeks(savings, balanceFinal = savingsSum)

### 4.2.4 - Plot joined savings summaries
fig, ax = plt.subplots()
ax.plot(summarySavA['WeeksAgo'], summarySavA['balanceFinal'], label = 'Savings, Personal')
ax.plot(summarySavS['WeeksAgo'], summarySavS['balanceFinal'], label = 'Savings, Shared')
ax.plot(summarySav['WeeksAgo'], summarySav['balanceFinal'], label = 'Savings, All')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
plt.xlim([104,0])
ax.legend()
plt.show()

### 4.2.5 - Join credit card debt summaries
credit = pd.concat([creditA, creditS], ignore_index = True, axis = 0)
credit = credit.sort_values(['Date'], ascending = False)
creditSum = creditA['Balance'].iloc[0] + creditS['Balance'].iloc[0]
summaryCredit = summarizeWeeks(credit, balanceFinal = creditSum)
### 4.2.5 - Plot joined credit card debt summaries
fig, ax = plt.subplots()
ax.plot(summaryCCA['WeeksAgo'], summaryCCA['balanceFinal'], label = 'Credit, Personal')
ax.plot(summaryCCS['WeeksAgo'], summaryCCS['balanceFinal'], label = 'Credit, Shared')
ax.plot(summaryCredit['WeeksAgo'], summaryCredit['balanceFinal'], label = 'Credit, All')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
plt.xlim([104,0])
ax.legend()
plt.show()

### 4.3 - Join all accounts
allAccounts = pd.concat([summaryChecking, summarySav, summaryCredit], ignore_index = True, axis = 0)
allAccounts = allAccounts.sort_values(['Date'], ascending = False)
allSum = summaryChecking['balanceFinal'].iloc[0] + summarySav['balanceFinal'].iloc[0] + summaryCredit['balanceFinal'].iloc[0]
summaryAll = summarizeWeeks(allAccounts, balanceFinal = allSum)

fig, ax = plt.subplots()
plt.gcf().set_size_inches(12, 8)
ax.plot(summaryChecking['Date'], summaryChecking['balanceFinal'], label = 'Checking', color = 'lightblue', linewidth = 2)
ax.plot(summarySav['Date'], summarySav['balanceFinal'], label = 'Savings', color = 'lightgreen', linewidth = 2)
ax.plot(summaryCredit['Date'], summaryCredit['balanceFinal'], label = 'Credit card debt', color = 'tomato', linewidth = 1)
ax.plot(summaryAll['Date'], summaryAll['balanceFinal'], label = 'All', color = 'navy', linewidth = 4)
plt.axhline(y = 0, color = 'black', linewidth = 1)
ax.set_xlabel('Date',  fontsize = 16)
ax.set_ylabel('Dollars', fontsize = 16)
ax.set_title('Balance over time', fontsize = 20)
ax.invert_xaxis()
plt.xticks(fontsize= 11, rotation = -30)
ax.yaxis.grid()
ax.xaxis.grid()
plt.xlim([104,0])
plt.ylim([-6000,20000])
#ax.set_xticks([0,10,20,30])
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
ax.legend(loc=2, prop={'size': 12})
plt.show()





################################################
############ IN PROGRESS ######################
################################################

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

### Sum of outflow
creditOutA = creditA.loc[creditA['Amount']<0]
creditOutA = creditOutA.loc[creditOutA['Date'] > datetime(2020,11,27)]
sum(creditOutA['Amount'])

creditOutS = creditS.loc[creditS['Amount']<0]
creditOutS = creditOutS.loc[creditOutS['Date'] > datetime(2020,11,27)]
sum(creditOutS['Amount'])

### Categorize AmEx spending
categories = np.array(creditS['Type'])
creditS['Type'].unique()



### 3 - Analysis

### For each week, determine the min, max, and number of withdrawls and deposits
### Identify the range covered in the data
dateStart = 
### Create a data frame with a row for each week

### 4 - Plotting



### 5 - Output


#### PRIOR CODE (DEPRECIATED)
###Summarize weeks


def summarizeWeeks(dataframe):
    dataframeSummary = pd.DataFrame(columns = ['WeeksAgo', 'balanceMin', 'balanceMax', 'balanceFinal','nOutflow', 'totalOutflow', 'nInflow', 'totalInflow', 'transactions'])
    weekRange = range(min(dataframe['WeeksAgo']), max(dataframe['WeeksAgo'] + 1))
    for week in weekRange:
        print('Week: ' + str(week))
        rowsSelected = dataframe['WeeksAgo'] == week
        subset = dataframe.loc[rowsSelected]
        if len(subset) == 0:
            newRow = pd.DataFrame({'WeeksAgo': [week], 'balanceMin': [balanceMin], 'balanceMax': [balanceMax], 'balanceFinal': [balanceFinal],'nOutflow': [0], 'totalOutflow': [0], 'nInflow': [0], 'totalInflow': [0], 'transactions': [0]})
        else:
            ### Save key stats:
            balanceMin = min(subset['Balance'])
            balanceMax = max(subset['Balance'])
            balanceFinal = subset['Balance'].iloc[0]
            outflows = subset.loc[subset['Amount'] <0]['Amount']
            totalOutflow = sum(outflows)
            nOutflow = len(outflows)
            
            inflows  = subset.loc[subset['Amount'] >0]['Amount']
            totalInflow = sum(inflows)
            nInflow = len(inflows)
        
            transactions = len(subset)
            newRow = pd.DataFrame({'WeeksAgo': [week], 'balanceMin': [balanceMin], 'balanceMax': [balanceMax], 'balanceFinal': [balanceFinal],'nOutflow': [nOutflow], 'totalOutflow': [totalOutflow], 'nInflow': [nInflow], 'totalInflow': [totalInflow], 'transactions': [transactions]})
    
        dataframeSummary = pd.concat([dataframeSummary,newRow], ignore_index = True, axis = 0)
    return(dataframeSummary)




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
    
### 3 - Plotting

### 3.1.1 - Plot checking account balances
fig, ax = plt.subplots()
ax.plot(checkingA['WeeksAgo'], checkingA['Balance'], label = 'Checking, Personal')
ax.plot(checkingS['WeeksAgo'], checkingS['Balance'], label = 'Checking, Shared')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
ax.legend()
plt.show()

### 3.1.1 - Plot SAVINGS account balances
fig, ax = plt.subplots()
ax.plot(savingsA['WeeksAgo'], savingsA['Balance'], label = 'savings, Personal')
ax.plot(savingsS['WeeksAgo'], savingsS['Balance'], label = 'savings, Shared')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
plt.xlim([104,0])
ax.legend()
plt.show()

### 3.1.1 - Plot CREDIT CARD DEBT balances
fig, ax = plt.subplots()
ax.plot(creditA['WeeksAgo'], creditA['Balance'], label = 'Credit card debt, Personal')
ax.plot(creditS['WeeksAgo'], creditS['Balance'], label = 'Credit card debt, Shared')
ax.set_xlabel('Weeks Ago',  fontsize = 12)
ax.set_ylabel('Dollars', fontsize = 12)
ax.set_title('Balance over time', fontsize = 12)
ax.invert_xaxis()
ax.legend()
plt.axis([104,0, min(creditS['Balance']), max(creditS['Balance'])])
plt.show()