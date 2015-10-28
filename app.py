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
    return sumDict



if __name__ == '__main__':
    rowList = parseCsv('harvest.csv')
    accounts = totalHours(rowList)
    apiUrl = discoverEndpoint()
    resultList = getAccounts(apiUrl)
    for i in range(len(resultList)):
        print resultList[i]['name'] +\
            ' - id: ' + str(resultList[i]['id'])
    for key in accounts:
        #print '|'.join(str(key).split(' '))
        regexp = re.compile('|'.join(str(key).split(' ')))

