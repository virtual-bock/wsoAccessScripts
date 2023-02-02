import sys
import time
import base64
import requests
import json
import datetime

#Get Bearer-Token for API-calls
def getBearer(wsoAccessTenant:str,wsoAccessAccount:str,wsoAccessSSecret:str):
    #Create Log file
    wsoLogfile = open (r'wsoAccess_'+ datetime.datetime.now().strftime("%m_%d_%Y") +'.log','a')
    #Build basic auth-header
    wsoBuild = ( wsoAccessAccount + ':'+ wsoAccessSSecret ).encode ('ascii')
    wsoAccessBasic = 'Basic ' + str(base64.b64encode ( wsoBuild ).decode ('ascii'))
    #Build url
    wsoAccessAuthUrl = 'https://' + wsoAccessTenant + '/SAAS/auth/oauthtoken?grant_type=client_credentials'
    wsoAccesspayload = {}
    #Build header
    authHeaders = {
      'Authorization': wsoAccessBasic,
      }
    authResponse = requests.request("POST", wsoAccessAuthUrl, headers=authHeaders, data=wsoAccesspayload)
    #print (authResponse.request.headers)
    #print (authResponse.status_code)
    #convert response to dictonary
    wsoAuthResponse = eval( authResponse.text )
    if authResponse.status_code != 200:
        wsoLogfile.write ( time.ctime() + ' Something went wrong. HTTP Statuscode was ' + str(authResponse.status_code) +'\n')
    else:
        wsoLogfile.write ( time.ctime() +' Token recived!\n')
    wsoLogfile.close ()
    return (wsoAuthResponse['access_token'])




#Get connected directorys 
def getDirectory(wsoAccessTenant:str,wsoAccessToken:str):
    wsoLogfile = open (r'wsoAccess_'+ datetime.datetime.now().strftime("%m_%d_%Y") +'.log','a')
    #Build url
    wsoAccessDictUrl = 'https://' + wsoAccessTenant + '/SAAS/jersey/manager/api/connectormanagement/directoryconfigs'
    wsoAccessDirectoryPayload = {}
    #Build Bearer-Token
    wsoAccessBearer = 'Bearer '+ wsoAccessToken
    #Build header
    wsoAccessBearerHeader = {
      'Authorization': wsoAccessBearer,
    }
    directoryResponse = requests.request("GET", wsoAccessDictUrl, headers=wsoAccessBearerHeader, data=wsoAccessDirectoryPayload)
    if directoryResponse.status_code !=200:
        wsoLogfile.write ( time.ctime() + ' Error: looks like you need a new bearer. HTTP error ' + str(directoryResponse.status_code) + '\n')
    else:
        wsoLogfile.write (directoryResponse.text)
    wsoLogfile.close()
    return (directoryResponse.text)




#Sync specific directory
def syncDirectory(wsoAccessTenant:str,wsoAccessToken:str,wsoAccessDirectory:str):
    wsoLogfile = open (r'wsoAccess_'+ datetime.datetime.now().strftime("%m_%d_%Y") +'.log','a')
    wsoAccessSyncUrl = 'https://' + wsoAccessTenant + '/SAAS/jersey/manager/api/connectormanagement/directoryconfigurations/'+ wsoAccessDirectory +'/sync/v2'
    #create a request-body
    wsoAccessSyncPayload = json.dumps({
        "ignoreSafeguards":"false"
    })
    wsoAccessBearer = 'Bearer '+ wsoAccessToken
    #Build header 
    wsoAccessSyncHeader = {
        'Authorization': wsoAccessBearer,
        'Accept':'application/vnd.vmware.horizon.manager.connector.management.directory.sync.trigger.v2+json',
        'Content-Type':'application/vnd.vmware.horizon.manager.connector.management.directory.sync.trigger.v2+json',
    }
    syncResponse = requests.request("POST", wsoAccessSyncUrl, headers=wsoAccessSyncHeader, data=wsoAccessSyncPayload)
    #print ( time.ctime() + ' ' + str(syncResponse.status_code))
    if syncResponse.status_code != 200:
        wsoLogfile.write ( time.ctime() + ' Something went wrong. HTTP Statuscode was ' + str(syncResponse.status_code) + '\n')
    else:
        wsoLogfile.write ( time.ctime() + ' Sync Successful!\n')
    wsoLogfile.close ()
    return (syncResponse.status_code)




#Warning: DELETE UEM connection data
def deleteWSOUEM_Config(wsoAccessTenant:str,wsoAccessToken:str):
    wsoLogfile = open (r'wsoAccess_'+ datetime.datetime.now().strftime("%m_%d_%Y") +'.log','a')
    wsoAccessRemoveUEMUrl = 'https://' + wsoAccessTenant + '/SAAS/jersey/manager/api/tenants/tenant/airwatchoptin/config'
    wsoAccessRemoveUEMPayload = {}
    wsoAccessBearer = 'Bearer '+ wsoAccessToken
    wsoAccessRemoveHeader = {
        'Authorization': wsoAccessBearer,
    }
    print ('Are you really sure to do this?')
    uemQuestion =sys.stdin ('Are you really sure to do this?(type yes in uppercase)')
    if uemQuestion == 'YES':
        removeResponse = requests.request("DELETE",wsoAccessRemoveUEMUrl, headers=wsoAccessRemoveHeader, data=wsoAccessRemoveUEMPayload)
        wsoLogfile.write ( time.ctime() + 'Configuration Removed! Statuscode ' + str(removeResponse.status_code) + '\n')
    else:
        print ("Nice that you don't want to delete the configuration.")
        wsoLogfile.write ( time.ctime() + ' Configuration not removed!\n')
    wsoLogfile.close ()
