import os
import urllib
import urllib2
import json
import datetime
import base64

### Retrieve API key from local file ./teamworkpm_api_key.txt
def getApiKey():
    curPath = os.getcwd()
    f = open('%s/api_key.txt' % curPath, 'rb')
    apikey = f.readline().strip()
    f.close()
    return apikey

def getUser():
    curPath = os.getcwd()
    f = open('%s/user_email.txt' % curPath, 'rb')
    useremail = f.readline().strip()
    f.close()
    return useremail

### Create authorization handler for TeamworkPM
def authUrl(theurl):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, getApiKey(), 'x')
    
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    
    opener = urllib2.build_opener(authhandler)
    
    urllib2.install_opener(opener)
    return

### GET request to establish parameters
def getUrl(theurl):
    
    authUrl(theurl)
    pagehandle = urllib2.urlopen(theurl)
    
    return pagehandle.read()

### POST request accepts the Teamwork-specific URL and a JSON object with      the necessary parameters for the action.
def postUrl(theurl, thePost):

    req = urllib2.Request(theurl)
    auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (getUser(), getApiKey()))
    req.add_header('Authorization', auth)
    req.add_header('Content-Type', 'application/json')
    req.add_header('id': '<id>', 'application/json')
    req.add_header('method': 'getLead', 'application/json')
#    req.add_header('params': { 'leadId': 1078 } }

    return urllib2.urlopen(req, json.dumps(thePost))

print postUrl('https://app01.nutshell.com/api/vq/json', { 'leadId': 1078 })
