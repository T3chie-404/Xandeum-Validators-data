#-------------------------------------------------------------------------------
# Name:         Xandeum Validator Data Capture
# Purpose:      Captures information about the Xandeum blockchain Validators
#
# Author:      John Spence
#
#
#
# Created:    
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

    payLoad = getClusterNodes()
    
    
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
        payLoadPrep = []
        #print (item['pubkey'], item['gossip'], item['version'])
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
    
    return(payLoad)

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
        #conn = mysql.connector.connect(**db_conn)        
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




#-------------------------------------------------------------------------------
#
#
#                                 MAIN SCRIPT
#
#
#-------------------------------------------------------------------------------

if setTest == 0:
    while True:
        if __name__ == "__main__":
            main()
        time.sleep(180)
else:
    if __name__ == "__main__":
        main()