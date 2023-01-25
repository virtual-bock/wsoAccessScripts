#import sys
#import time
import base64
import requests
import json

def getBearer(wsoAccessTenant,wsoAccessAccount,wsoAccessSSecret):
    #Build basic auth-header
    wsoBuild = ( wsoAccessAccount + ':'+ wsoAccessSSecret ).encode ('ascii')
    wsoAccessBasic = 'Basic ' + str(base64.b64encode ( wsoBuild ).decode ('ascii'))
    #Build auth-url
    wsoAccessAuthUrl = 'https://' + wsoAccessTenant + '/SAAS/auth/oauthtoken?grant_type=client_credentials'
    wsoAccesspayload = {}
    authHeaders = {
      'Authorization': wsoAccessBasic,
      }
    #integrate simple logging (todo)
    authResponse = requests.request("POST", wsoAccessAuthUrl, headers=authHeaders, data=wsoAccesspayload)
    print (authResponse.request.headers)
    print (authResponse.status_code)
    #convert response to dictonary
    wsoAuthResponse = eval(authResponse.text)
    if authResponse.status_code != 200:
        print ('Something went wrong. HTTP Statuscode was ' + authResponse.status_code)
        #integrate a simple logging (todo)
    else:
        print ('Token recived!')
    return (wsoAuthResponse['access_token'])





def getDirectory(wsoAccessTenant,wsoAccessToken,):
    
    wsoAccessDictUrl = 'https://' + wsoAccessTenant + '/SAAS/jersey/manager/api/connectormanagement/directoryconfigs'
    
    wsoAccessDirectoryPayload={}
 
    wsoAccessBearer = 'Bearer '+ wsoAccessToken
    print (wsoAccessBearer)
 
    wsoAccessBearerHeader={
      'Authorization': wsoAccessBearer,
    }
    
    directoryResponse = requests.request("GET", wsoAccessDictUrl, headers=wsoAccessBearerHeader, data=wsoAccessDirectoryPayload)
    if directoryResponse.status_code !=200:
        print('Error: looks like you need a new bearer. HTTP error '+ str(directoryResponse.status_code))
    else:
        print(directoryResponse.text)





def syncDirectory(wsoAccessTenant,wsoAccessToken,wsoAccessDirectory):
    wsoAccessSyncUrl = 'https://' + wsoAccessTenant + '/SAAS/jersey/manager/api/connectormanagement/directoryconfigurations/'+ wsoAccessDirectory +'/sync/v2'
    wsoAccessSyncPayload = json.dumps({
        "ignoreSafeguards":"false"
    })
    wsoAccessBearer = 'Bearer '+ wsoAccessToken
    print (wsoAccessBearer)
    wsoAccessSyncHeader = {
    'Authorization': wsoAccessBearer,
    'Accept':'application/vnd.vmware.horizon.manager.connector.management.directory.sync.trigger.v2+json',
    'Content-Type':'application/vnd.vmware.horizon.manager.connector.management.directory.sync.trigger.v2+json',
    }
    
    syncResponse = requests.request("POST", wsoAccessSyncUrl, headers=wsoAccessSyncHeader, data=wsoAccessSyncPayload)
    print (syncResponse.status_code)
    if syncResponse.status_code != 200:
        print ('Something went wrong. HTTP Statuscode was ' + str(syncResponse.status_code))
        #integrate a simple logging (todo)
    else:
        print ('Sync Successful')
