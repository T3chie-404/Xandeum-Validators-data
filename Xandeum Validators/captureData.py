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

# Open Data Source
dataSource = r'https://services1.arcgis.com/EYzEZbDhXZjURPbP/arcgis/rest/services/Bellevue_Permits/FeatureServer/0'


# ------------------------------------------------------------------------------
# DO NOT UPDATE BELOW THIS LINE OR RISK DOOM AND DISPAIR!  Have a nice day!
# ------------------------------------------------------------------------------

import datetime
import time
import base64
import urllib
import requests
import json
import sys
import os

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


#-------------------------------------------------------------------------------
#
#
#                                 MAIN SCRIPT
#
#
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    main()