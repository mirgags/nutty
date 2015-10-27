from nutshellapi import *

theJson = { "method": "getApiForUsername",
            "params": {"username": "nutshelladmin@pint.com"},
            "id": "apeye"
          }
res = postUrl('http://api.nutshell.com/v1/json', theJson)
print res.code
resJson = json.loads(res.read())
print resJson
apiEndpoint = 'https://' + resJson['result']['api'] + '/api/v1/json'
print apiEndpoint
#theJson = { "method": "findAccountTypes", "id": "apeye" }
theJson = { "method": "findAccounts",
            "params": {
                "accountType": [ 1, 33, 25, 29 ],
                "limit": 100
            },
            "id": "apeye" }
res = postUrl(apiEndpoint, theJson)
resJson = json.loads(res.read())
for i in range(len(resJson['result'])):
    print resJson['result'][i]['name'] +\
        ' - id: ' + str(resJson['result'][i]['id'])
#print res.read()
