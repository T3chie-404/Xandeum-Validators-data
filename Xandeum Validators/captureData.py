#-------------------------------------------------------------------------------
# Name:         Xandeum Validator Data Capture
# Purpose:      Captures information about the Xandeum blockchain Validators
#
# Author:      John Spence
#
#
#
# Created:  2023-09-06
# Modified:   
# Modification Purpose: 
#
#
#-------------------------------------------------------------------------------


# 888888888888888888888888888888888888888888888888888888888888888888888888888888
# ------------------------------- Configuration --------------------------------
#   Adjust the settings below to match your org. eMail functionality is not 
#   present currently, though obviously can be built in later.
#
# ------------------------------- Dependencies ---------------------------------
#
#
#
# 888888888888888888888888888888888888888888888888888888888888888888888888888888

import datetime
from pickletools import read_stringnl_noescape_pair
from smtplib import quoteaddr
import time
import base64
import requests
import json
import sys
import os
import mysql.connector
from mysql.connector.constants import ClientFlag
from dotenv import find_dotenv, load_dotenv

# ------------------------------------------------------------------------------
# DO NOT UPDATE BELOW THIS LINE OR RISK DOOM AND DISPAIR!  Have a nice day!
# ------------------------------------------------------------------------------

envPath = find_dotenv()
load_dotenv(envPath)

# Testing & Research settings
setTest = os.getenv('setTest')

# Validator Data Source Options
dataSources = os.getenv('dataSources')
dataSourcePorts = os.getenv('dataSourcePorts')

# Data Store Configuration
dbase = os.getenv('dbase')
dbPort = os.getenv('dbPort')
dbName = os.getenv('dbName')
dbUname = os.getenv('dbUname')
dbPass = os.getenv('dbPass')


# Configure hard coded db connection here.
db_conn = {
    'host':dbase,
    'database':dbName,
    'port':dbPort,        
    'user':dbUname,    
    'password':dbPass
    }

#-------------------------------------------------------------------------------
#
#
#                                 Functions
#
#
#-------------------------------------------------------------------------------

def main():
#-------------------------------------------------------------------------------
# Name:        Function - main
# Purpose:  Starts the whole thing.
#-------------------------------------------------------------------------------

    starttime = startup()
    print ('Starup job @: {}'.format(starttime))

    try:
        getClusterNodes()
        getEpochInfo()
    except:
        time.sleep (10)
        print ('-- Temporary failure. Trying again in a few minutes.')
    
    stoptime = startup()    
    print ('Finished job @: {}'.format(stoptime))

    return

def startup():
#-------------------------------------------------------------------------------
# Name:        Function - main
# Purpose:  Starts the whole thing.
#-------------------------------------------------------------------------------

    starttime = datetime.datetime.now()

    return (starttime)


def captureData(values):
#-------------------------------------------------------------------------------
# Name:        Function - captureData
# Purpose:  
#-------------------------------------------------------------------------------
  
    urlQuery = 'http://{}:{}'.format(dataSources, dataSourcePorts)
    headers = {
        'Content-Type': 'application/json'
        }
    dataResponse = requests.post(urlQuery, headers=headers, json=values)
    
    dataJSON = dataResponse.json()        
        
    return (dataJSON)


def getClusterNodes():
#-------------------------------------------------------------------------------
# Name:        Function - getClusterNodes
# Purpose:  
#-------------------------------------------------------------------------------

    values = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getClusterNodes'
        }

    dataJSON = captureData(values)
    
    print ('There are {} potential validators reporting in.'.format(len(dataJSON['result'])))
    
    payLoad = []        
    for item in dataJSON['result']:
        valID = item['pubkey']
        valGoss = item['gossip']
        valIP = valGoss.split(':', 1)[0]
        valPort = valGoss.split(':', 1)[1]
        valVer = item['version']
        print ('Found Validatior ID {} \n\t'.format(valID), 
               '-- IP Address: {} \n\t'.format(valIP),
               '-- IP Port: {} \n\t'.format(valPort),
               '-- RPC Address: {} \n\t'.format(valGoss),
               '-- Validator Version: {} \n\n'.format(valVer))
        payLoadPrep = (valID, valGoss, valIP, valPort, valVer)
        payLoad.append(payLoadPrep)      

    storeClusterNodes(payLoad)
    
    return()

def getEpochInfo():
#-------------------------------------------------------------------------------
# Name:        Function - getEpochInfo
# Purpose:  
#-------------------------------------------------------------------------------    
    
    values = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getEpochInfo'
        }

    dataJSON = captureData(values)
    
    payLoad = []
    valEpoch = int(dataJSON['result']['epoch'])
    valSlots = int(dataJSON['result']['slotsInEpoch'])
    valTransactions = int(dataJSON['result']['transactionCount'])
    print ('Found Epoch ID {} \n\t'.format(valEpoch),
            '-- Slots in Epoch: {} \n\t'.format(valSlots),
            '-- Current Tranasaction Count: {} \n\n'.format(valTransactions)               
            )
    payLoadPrep = (valEpoch, valSlots, valTransactions)
    payLoad.append(payLoadPrep)
    
    newData = storeEpochInfo(payLoad)
    
    if newData != 0:
        getVoteAccounts(valEpoch)
    
    return()

def getVoteAccounts(valEpoch):
#-------------------------------------------------------------------------------
# Name:        Function - getVoteAccounts
# Purpose:  
#-------------------------------------------------------------------------------
    
    values = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getVoteAccounts'
        }

    dataJSON = captureData(values)
    
    for item in dataJSON['result']['current']:
        payLoad = []
        valID = item['nodePubkey']
        valVoteID = item['votePubkey']
        valCommission = item['commission']
        valActiveStake = item['activatedStake']
        valLastVote = item['lastVote']
        valCurrent = 'Current'
        valVotes = item['epochCredits']
        
        print ('Found Validator ID {} \n\t'.format(valID),
                '-- Vote Account: {} \n\t'.format(valVoteID),
                '-- Commission: {} \n\t'.format(valCommission),
                '-- Stake: {} \n\t'.format(valActiveStake),
                '-- Last Voted: {} \n\t'.format(valLastVote),
                '-- Current: {} \n\t'.format(valCurrent),
                '-- Recent Votes: {} \n\n'.format(valVotes)
                )
        payLoadPrep = (valID, valVoteID, valCommission, valActiveStake, 
                       valLastVote, valCurrent)
        payLoad.append(payLoadPrep)

        itemFKID = storeVoteAccount(payLoad)

        storeVotes (itemFKID, valEpoch, valVotes)

        
    for item in dataJSON['result']['delinquent']:
        payLoad = []        
        valID = item['nodePubkey']
        valVoteID = item['votePubkey']
        valCommission = item['commission']
        valActiveStake = item['activatedStake']
        valLastVote = item['lastVote']
        valCurrent = 'Delinquent'
        valVotes = item['epochCredits']        
        
        print ('Found Validator ID {} \n\t'.format(valID),
                '-- Vote Account: {} \n\t'.format(valVoteID),
                '-- Commission: {} \n\t'.format(valCommission),
                '-- Stake: {} \n\t'.format(valActiveStake),
                '-- Last Voted: {} \n\t'.format(valLastVote),
                '-- Current: {} \n\t'.format(valCurrent),
                '-- Recent Votes: {} \n\n'.format(valVotes)
                )
        payLoadPrep = (valID, valVoteID, valCommission, valActiveStake, 
                       valLastVote, valCurrent)
        payLoad.append(payLoadPrep)
        
        itemFKID = storeVoteAccount(payLoad)

        storeVotes (itemFKID, valEpoch, valVotes)
      
                 
    return()

def storeClusterNodes(payLoad):
#-------------------------------------------------------------------------------
# Name:        Function - storeClusterNodes
# Purpose:  
#-------------------------------------------------------------------------------

    conn = mysql.connector.connect(**db_conn)    

    for item in payLoad:
        valID = item[0]
        valGoss = item[1]
        valIP = item[2]
        valPort = item[3]
        valVer = item[4]
        
        checkRes = checkIfValidatorExists(conn, valID)    
        if checkRes == 0:            
            query = conn.cursor()
            sqlCommand = '''

            insert into validators (
                validatorID
                , firstCaptureDate
                , sysCreateDate
                , sysChangeDate
                , globalID
            )
                Values ('{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), UUID())

            '''.format(valID)

            query.execute(sqlCommand)           
            conn.commit()
        else:   
            conn = mysql.connector.connect(**db_conn)            
            query = conn.cursor()
            sqlCommand = '''

            update validators
            set sysChangeDate = CURRENT_TIMESTAMP()
            where validatorID = '{}'

            '''.format(valID)

            query.execute(sqlCommand)
            conn.commit()
            
        itemFKID = gatherValidatorFKID(conn, valID)
        captureValidatorConfig(conn, itemFKID, valGoss, valIP, valPort, valVer)
        
    conn.close()

    return()

def checkIfValidatorExists(conn, valID):
#-------------------------------------------------------------------------------
# Name:        Function - checkIfExists
# Purpose:  
#-------------------------------------------------------------------------------
  
    checkRes = 0
    query = conn.cursor()
    query_string = '''
    
    SELECT COUNT(validatorID) FROM validators 
    WHERE validatorID = '{}'
        
    '''.format(valID)
    
    query.execute(query_string)
    queryResult = query.fetchone()
    
    testItem = queryResult[0]
    
    if testItem == 0:
        checkRes = 0
    else: 
        checkRes = 1
        
    query.close() 
    
    return(checkRes)


def gatherValidatorFKID(conn, valID):
#-------------------------------------------------------------------------------
# Name:        Function - checkIfExists
# Purpose:  
#-------------------------------------------------------------------------------

    query = conn.cursor()
    query_string = '''
    
    SELECT globalID FROM validators 
    WHERE validatorID = '{}'
        
    '''.format(valID)
    
    query.execute(query_string)
    queryResult = query.fetchone()
    
    itemFKID = queryResult[0]
        
    query.close()
    
    return(itemFKID)

def captureValidatorConfig(conn, itemFKID, valGoss, valIP, valPort, valVer):
#-------------------------------------------------------------------------------
# Name:        Function - captureValidatorConfig
# Purpose:  
#-------------------------------------------------------------------------------
    
    query = conn.cursor()
    query_string = '''
    
    SELECT globalID FROM validatorsConfig 
    WHERE fkID = '{}' order by sysChangeDate desc
        
    '''.format(itemFKID)
 
    query.execute(query_string)
    queryResult = query.fetchone() 
    
    if queryResult != None:
        itemGLID = queryResult[0]
        query = conn.cursor()
        query_string = '''
    
        SELECT ipAddress FROM validatorsConfig 
        WHERE globalID = '{}' order by sysChangeDate desc
        
        '''.format(itemGLID)
 
        query.execute(query_string)
        queryResult = query.fetchone()
        itemIP = queryResult[0]
        if itemIP != valIP:
            query = conn.cursor()
            sqlCommand = '''

            insert into validatorsConfig (
                fkID
                , gossip
                , ipAddress
                , port
                , validatorVersion
                , sysCreateDate
                , sysChangeDate
                , globalID
            )
                Values ('{}', '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), UUID())

            '''.format(itemFKID, valGoss, valIP, valPort, valVer)

            query.execute(sqlCommand)           
            conn.commit()
        else:
            query = conn.cursor()
            sqlCommand = '''

            update validatorsConfig
            set sysChangeDate = CURRENT_TIMESTAMP()
                , port = '{}'
                , gossip = '{}'
                , validatorVersion = '{}'
            where globalID = '{}'
            '''.format(valPort, valGoss, valVer, itemGLID)
            query.execute(sqlCommand)
            conn.commit()                       
    else:
        query = conn.cursor()
        sqlCommand = '''

        insert into validatorsConfig (
            fkID
            , gossip
            , ipAddress
            , port
            , validatorVersion
            , sysCreateDate
            , sysChangeDate
            , globalID
        )
            Values ('{}', '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), UUID())

        '''.format(itemFKID, valGoss, valIP, valPort, valVer)

        query.execute(sqlCommand)           
        conn.commit()       
        
    query.close()
    
    
    return()

def storeEpochInfo(payLoad):
#-------------------------------------------------------------------------------
# Name:        Function - storeEpochInfo
# Purpose:  
#-------------------------------------------------------------------------------

    conn = mysql.connector.connect(**db_conn)
    
    for item in payLoad:
        valEpoch = item[0]
        valSlots = item[1]
        valTransactions = item[2]
        
        checkRes = checkIfEpochExists(conn, valEpoch)
        
        if checkRes == 0:            
            query = conn.cursor()
            sqlCommand = '''

            insert into epochInfo (
                epoch
                , slots
                , transactionCount
                , sysCreateDate
                , sysChangeDate
                , globalID
            )
                Values ({}, {}, {}, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), UUID())

            '''.format(valEpoch, valSlots , valTransactions)

            query.execute(sqlCommand)           
            conn.commit()

            newData = 1            

        else:   
            conn = mysql.connector.connect(**db_conn)            
            query = conn.cursor()
            sqlCommand = '''

            update epochInfo
            set sysChangeDate = CURRENT_TIMESTAMP()
            , transactionCount = {}
            where epoch = {}

            '''.format(valTransactions, valEpoch)

            query.execute(sqlCommand)
            conn.commit()
            
            newData = 0
    
    conn.close()

    return(newData)

def checkIfEpochExists(conn, valEpoch):
#-------------------------------------------------------------------------------
# Name:        Function - checkIfEpochExists
# Purpose:  
#-------------------------------------------------------------------------------
  
    checkRes = 0
    query = conn.cursor()
    query_string = '''
    
    SELECT COUNT(epoch) FROM epochInfo 
    WHERE epoch = {}
        
    '''.format(valEpoch)
    
    query.execute(query_string)
    queryResult = query.fetchone()
    
    testItem = queryResult[0]
    
    if testItem == 0:
        checkRes = 0
    else: 
        checkRes = 1
        
    query.close() 
    
    return(checkRes)

def storeVoteAccount(payLoad):
#-------------------------------------------------------------------------------
# Name:        Function - storeVoteAccount
# Purpose:  
#-------------------------------------------------------------------------------

    conn = mysql.connector.connect(**db_conn)
    
    for item in payLoad:
        valID = item[0]
        valVoteID = item[1]
        valCommission = item[2]
        valActiveStake = item[3]
        valLastVote = item[4]
        valCurrent = item[5]
        
        checkRes = checkIfValidatorExists(conn, valID)
        
        if checkRes == 0:                     
            query = conn.cursor()
            sqlCommand = '''

            insert into validators (
                validatorID
                , firstCaptureDate
                , sysCreateDate
                , sysChangeDate
                , globalID
            )
                Values ('{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), UUID())

            '''.format(valID)

            query.execute(sqlCommand)           
            conn.commit()

            query = conn.cursor()
            query_string = '''
    
            SELECT globalID FROM validators 
            WHERE validatorID = '{}'
        
            '''.format(valID)
    
            query.execute(query_string)
            queryResult = query.fetchone()
    
            itemFKID = queryResult[0]

            sqlCommand = '''

            insert into votingValidators (
                validatorID
                , voteID
                , commission
                , activatedStake
                , lastVote
                , current
                , sysCreateDate
                , sysChangeDate
                , fkID
                , globalID
            )
                Values ('{}', '{}', {}, {}, {}, '{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '{}', UUID())

            '''.format(valID, valVoteID, valCommission, valActiveStake, valLastVote, valCurrent, itemFKID)

            query.execute(sqlCommand)           
            conn.commit()           

        else:            
            checkRes = checkIfValVotePairExists(conn, valID, valVoteID)
            if checkRes == 0:
                query = conn.cursor()
                query_string = '''
    
                SELECT globalID FROM validators 
                WHERE validatorID = '{}'
        
                '''.format(valID)
    
                query.execute(query_string)
                queryResult = query.fetchone()
    
                itemFKID = queryResult[0]                

                sqlCommand = '''

                insert into votingValidators (
                    validatorID
                    , voteID
                    , commission
                    , activatedStake
                    , lastVote
                    , current
                    , sysCreateDate
                    , sysChangeDate
                    , fkID
                    , globalID
                )
                    Values ('{}', '{}', {}, {}, {}, '{}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '{}', UUID())

                '''.format(valID, valVoteID, valCommission, valActiveStake, valLastVote, valCurrent, itemFKID)

                query.execute(sqlCommand)           
                conn.commit()

            else:
               
                conn = mysql.connector.connect(**db_conn)            
                query = conn.cursor()
                sqlCommand = '''

                update votingValidators
                set commission = {}
                , activatedStake = {}
                , lastVote = {}
                , current = '{}'
                , sysChangeDate = CURRENT_TIMESTAMP()
                where validatorID = '{}' and voteID = '{}'

                '''.format(valCommission, valActiveStake, valLastVote, valCurrent, valID, valVoteID)

                query.execute(sqlCommand)
                conn.commit()
                
        query = conn.cursor()
        query_string = '''
    
        SELECT globalID FROM votingValidators 
        where validatorID = '{}' and voteID = '{}'
        
        '''.format(valID, valVoteID)
    
        query.execute(query_string)
        queryResult = query.fetchone()
    
        itemFKID = queryResult[0]
            
    query.close
    conn.close()

    return(itemFKID)

def checkIfValVotePairExists(conn, valID, valVoteID):
#-------------------------------------------------------------------------------
# Name:        Function - checkIfExists
# Purpose:  
#-------------------------------------------------------------------------------
  
    checkRes = 0
    query = conn.cursor()
    query_string = '''
    
    SELECT COUNT(validatorID) FROM votingValidators 
    WHERE validatorID = '{}' and voteID = '{}'
        
    '''.format(valID, valVoteID)
    
    query.execute(query_string)
    queryResult = query.fetchone()
    
    testItem = queryResult[0]
    
    if testItem == 0:
        checkRes = 0
    else: 
        checkRes = 1
        
    query.close() 
    
    return(checkRes)

def storeVotes (itemFKID, valEpoch, valVotes):
#-------------------------------------------------------------------------------
# Name:        Function - storeVotes
# Purpose:  
#-------------------------------------------------------------------------------

    conn = mysql.connector.connect(**db_conn)
    
    for vote in valVotes:
        valVoteEpoch = vote[0]
        valCreditsStart = vote[1]
        valCreditsFinish = vote[2]
        
        if valVoteEpoch != valEpoch:
            checkRes = checkIfVoteExists(conn, itemFKID, valVoteEpoch)
            
            if checkRes == 0:                     
                query = conn.cursor()
                sqlCommand = '''

                insert into votingValidatorVotes (
                    epoch
                    , credits
                    , previousCredits
                    , sysCreateDate
                    , sysChangeDate
                    , fkID
                    , globalID
                )
                    Values ({}, {}, {}, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '{}', UUID())

                '''.format(valVoteEpoch, valCreditsStart, valCreditsFinish, itemFKID)

                query.execute(sqlCommand)           
                conn.commit()
                
    return()

def checkIfVoteExists(conn, itemFKID, valVoteEpoch):
#-------------------------------------------------------------------------------
# Name:        Function - checkIfEpochExists
# Purpose:  
#-------------------------------------------------------------------------------
  
    checkRes = 0
    query = conn.cursor()
    query_string = '''
    
    SELECT COUNT(epoch) FROM votingValidatorVotes 
    WHERE epoch = {} and fkID = '{}'
        
    '''.format(valVoteEpoch, itemFKID)
    
    query.execute(query_string)
    queryResult = query.fetchone()
    
    testItem = queryResult[0]
    
    if testItem == 0:
        checkRes = 0
    else: 
        checkRes = 1
        
    query.close() 
    
    return(checkRes)


#-------------------------------------------------------------------------------
#
#
#                                 MAIN SCRIPT
#
#
#-------------------------------------------------------------------------------

if setTest == 'False':
    while True:
        if __name__ == "__main__":
            main()
        time.sleep(180)
else:
    if __name__ == "__main__":
        main()