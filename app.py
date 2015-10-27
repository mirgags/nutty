from nutshellapi import *
import csv, re

def parseCsv(csvFile):
    theList = []
    with open(csvFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            theList.append(row)
    return theList

def webCalls():
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

if __name__ == '__main__':
    rowList = parseCsv('harvest.csv')
    sumDict = {}
    for row in rowList:
        if rowList.index(row) > 0:
            try:
                sumDict[row[1]][row[2]] += float(row[16].replace(',',''))
            except KeyError:
                try:
                    sumDict[row[1]][row[2]] = float(row[16].replace(',',''))
                except KeyError:
                    sumDict[row[1]] = { row[2]: float(row[16].replace(',','')) }
    regexp = re.compile('maintenance|t\/m', re.I)
    for key in sumDict:
        total = 0.0
        for subKey in sumDict[key]:
            #matchObj = regexp.search(subKey)
            #if matchObj:
            total += sumDict[key][subKey]
                #print key + ' total: ' + str(total)
        sumDict[key]['Total'] = total
    for key in sumDict:
        print key + ': ' + json.dumps(sumDict[key]) + '\n\n'

