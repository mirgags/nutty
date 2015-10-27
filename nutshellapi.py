import os
import urllib
import urllib2
import json
import datetime
import base64

### Retrieve API key from local file ./config.json
def getConfig():
    curPath = os.getcwd()
    f = open('%s/config.json' % curPath, 'rb')
    theJson = json.load(f)
    f.close()
    #for key in theJson:
        #print str(key) + ': ' + theJson[key]
    return theJson

### Create authorization handler for Nutshell
def authUrl(theurl):
    config = getConfig()
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, config[username], config[api_key])
    
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
    config = getConfig()
    print json.dumps(config)
    user = config['username']
    password = config['api_key']
    auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (user, password))
    req.add_header('Authorization', auth)
    req.add_header('Content-Type', 'application/json')
    #req.add_header('id': '<id>', 'application/json')
    #req.add_header('method': 'getLead', 'application/json')
#    req.add_header('params': { 'leadId': 1078 } }

    return urllib2.urlopen(req, json.dumps(thePost))

