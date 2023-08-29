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
import time
import base64
import requests
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

# ------------------------------------------------------------------------------
# DO NOT UPDATE BELOW THIS LINE OR RISK DOOM AND DISPAIR!  Have a nice day!
# ------------------------------------------------------------------------------

envPath = find_dotenv()
load_dotenv(envPath)

# Validator Data Source Options
dataSources = os.getenv('dataSources')
dataSourcePorts = os.getenv('dataSourcePorts')

# Data Store Configuration
dbase = os.getenv('dbase')
dbName = os.getenv('dbName')
dbUname = os.getenv('dbUname')
dbPass = os.getenv('dbPass')

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

    getClusterNodes()
    
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
# Name:        Function - captureDS
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
# Name:        Function - captureDS
# Purpose:  
#-------------------------------------------------------------------------------

    values = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getClusterNodes'
        }

    dataJSON = captureData(values)
    
    for item in dataJSON['result']:
        print (item['pubkey'], item['gossip'], item['version'])
    
    return()


#-------------------------------------------------------------------------------
#
#
#                                 MAIN SCRIPT
#
#
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    main()