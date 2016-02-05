import os
import urllib
import urllib2
import json
import datetime
import base64
import requests

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

### POST request accepts the Nutshell URL and a JSON object with the necessary parameters for the action.
def postUrl(theurl, thePost):

    req = urllib2.Request(theurl)
    config = getConfig()
    #print json.dumps(config)
    user = config['username']
    password = config['api_key']
    auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (user, password))
    req.add_header('Authorization', auth)
    req.add_header('Content-Type', 'application/json')

    return urllib2.urlopen(req, json.dumps(thePost))

def discoverEndpoint():
    config = getConfig()
    theJson = { "method": "getApiForUsername",
                "params": {"username": config['username']},
                "id": "apeye"
              }
    res = postUrl('http://api.nutshell.com/v1/json', theJson)
    #print res.code
    resJson = json.loads(res.read())
    #print resJson
    apiEndpoint = 'https://' + resJson['result']['api'] + '/api/v1/json'
    #print apiEndpoint
    return apiEndpoint

def findLeadOutcomes(apiEndpoint):
    theJson = {
        "method": "findLead_Outcomes"
    }
    res = postUrl(apiEndpoint, theJson)
    print res.read()
    try:
        return json.loads(res.read())
    except:
        return { "response": "no JSON response received" }

def createLead(apiEndpoint, data=None):
    config = getConfig()
    print json.dumps(config)
    user = config['username']
    password = config['api_key']
    auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (user, password))
    headers = {
    'authorization': auth,
    'content-type': 'application/json',
    'accept-encoding': '*'
    }
    theJson = {
        "method": "newLead",
        "params": data
    }
    #res = postUrl(apiEndpoint, theJson)
    resCreate = requests.post(apiEndpoint, headers=headers, json=theJson)
    print "Headers sent:"
    print resCreate.request.headers
    print "Response Code:"
    print resCreate.status_code
    print resCreate.headers
    print resCreate.cookies
    try:
        print "Response JSON:\n" + json.dumps(resJson.json())
    except:
        print "Response JSON: None\n"

    try:
        return resJson.json()
    except:
        return { "response": "no JSON response received" }

def editLead(apiEndpoint, leadId, revId, data=None):
    theJson = {
        "method": "editLead",
        "params": {
            "leadId": leadId,
            "rev": revId,
            "lead": data["lead"]
        }
    }
    res = postUrl(apiEndpoint, revId, theJson)
    try:
        return json.loads(res.read())
    except:
        return { "response": "no JSON response received" }

def getLastLead(apiEndpoint):
    config = getConfig()
    user = config['username']
    password = config['api_key']
    auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (user, password))
    headers = {
    'authorization': auth,
    'content-type': 'application/json'
    }
    theJson = {
        "method": "findLeads",
        "params": {
            "query": {"status": 0},
            "orderBy": "id",
            "limit": 1
        }
    }
    resCreate = requests.post(apiEndpoint, headers=headers, data=json.dumps(theJson))
    print "Response Code: " + str(resCreate.status_code)
    try:
        return resCreate.json()
    except:
        return {"response": "No JSON returned"}


def getProducts(apiEndpoint):
    theJson = { "method": "findProducts",
                "params": [],
                "id": "apeye" }
    res = postUrl(apiEndpoint, theJson)
    print 'Response Code: ' + res.code
    return json.loads(res.read())

def getAccounts(apiEndpoint, page=None, resultList=None):
    if resultList:
        result = resultList
    else:
        result = []
    if page:
        page = page
    else:
        page = 1
    theJson = { "method": "findAccounts",
                "params": {
                    "accountType": [ 1, 33, 25, 29 ],
                    "limit": 100,
                    "page": page
                },
                "id": "apeye" }
    res = postUrl(apiEndpoint, theJson)
    resJson = json.loads(res.read())
    for i in range(len(resJson['result'])):
        result.append(resJson['result'][i])
    if len(resJson['result']) < theJson['params']['limit']:
        return result
    else:
        return getAccounts(apiEndpoint, page + 1, result)
