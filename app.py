from nutshellapi import *

theJson = { "method": "getApiForUsername",
            "params": {"username": "nutshelladmin@pint.com"},
            "id": "apeye"
          }
res = postUrl('http://api.nutshell.com/v1/json', theJson)
print res.code
print res.read()
