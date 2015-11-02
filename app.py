from nutshellapi import *
import csv, re

def parseCsv(csvFile):
    theList = []
    with open(csvFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            theList.append(row)
    return theList

def totalHours(rowList):
    with open('accounts.json', 'rb') as f:
        sumDict = json.load(f)
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
            if subKey != 'Total' and subKey != 'id':
                total += sumDict[key][subKey]
                #print key + ' total: ' + str(total)
        sumDict[key]['Total'] = total
        if not 'id' in sumDict[key]:
            sumDict[key]['id'] = ''
    for key in sumDict:
        print key + ': ' + json.dumps(sumDict[key]) + '\n\n'
    return sumDict



if __name__ == '__main__':
    ### Import report from Harvest CSV file
    rowList = parseCsv('harvest.csv')

    ### Sum projects in unified Account JSON
    accounts = totalHours(rowList)

    ### PrettyPrint Accounts to JSON
    #with open('accounts.json', 'wb') as f:
    #    json.dump(accounts, f, indent=4, sort_keys=True)
    #f.close()

    ### Get Nutshell API Endpoint
    apiUrl = discoverEndpoint()

    ### Get Products List (for reference only, now)
    #products = getProducts(apiUrl)
    #print json.dumps(products)

    with open('accounts.json', 'rb') as f:
        theJson = json.load(f)

    count = 0
    for key in theJson:
        if count < 3 and theJson[key]['Total'] > 0:
            companyID = theJson[key]['id']
            totalHours = theJson[key]['Total']
        
            ### Set Lead JSON - Default USer is Admin
            ### Want to create all these fields, but API blocks them
            data = {
                "lead": {
                    "primaryAccount": {"id": companyID},
                    "name": "3Q2015 Maintenance",
                    "status": 10,
                    "createdTime": "2015-07-01T00:10:01-01:00",
                    "dueTime": "2015-09-30T23:59:19-05:00",
                    "products": [
                        {
                            "quantity": 1,
                            "price": {
                                "currency_shortname": "USD",
                                "amount": str(totalHours)
                            },
                            "id": 41
                        }
                    ],
                    "assignee": {
                        "entityType": "Users",
                        "id": 29
                    }
                }
            }
            ### Creating modified Leads until Nutshell Support responds
            data = {
                "lead": {
                    "primaryAccount": {"id": companyID},
                    "dueTime": "2015-09-30T23:59:19-05:00",
                    "tags": [ "PINT Maintenance"],
                    "products": [
                        {
                            "quantity": 1,
                            "price": {
                                "currency_shortname": "USD",
                                "amount": str(totalHours)
                            },
                            "id": 41
                        }
                    ],
                    "assignee": {
                        "entityType": "Users",
                        "id": 29
                    }
                }
            }
            res = createLead(apiUrl, data)
            #print json.dumps(res)
        count += 1

    ### Get Account information from Nutshell with some broken regex stuff for the future
    #resultList = getAccounts(apiUrl)
    #for i in range(len(resultList)):
    #    print resultList[i]['name'] +\
    #        ' - id: ' + str(resultList[i]['id'])
    #    for key in accounts:
    #        #print '|'.join(str(key).split(' '))
    #        regexp = re.compile('|'.join(str(key).split(' ')))
    #        matchObj = regexp.search(resultList[i]['name'], re.I)
    #        if matchObj:
    #            print 'We matched ' + resultList[i]['name'] + ' with ' + key + ' based on:'
    #            print matchObj.groups()
    #        matchObj = None
