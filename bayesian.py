#encoding=utf-8

#
#
# Pr(H | T) = Pr(T | H) / [Pr(T | H) + Pr( T | M)]
# P(A|t1, t2, t3 ... tn) = (P1 * P2 * ... * PN) / [P1 * P2 * ... * PN + (1 - P1) * (1 - P2) * ... * (1 - PN)]

import jieba


def tokensFromString(string):
    return list(jieba.cut(string, cut_all=False))


def addTokensToCountTable(tokens, countTable):
    for token in tokens:
        temp = token.encode("UTF-8", errors="strict")
        countTable[temp] = 1


def totalCountFromCountTable(countTable):
    totalCount = 0
    for key in countTable:
        totalCount += countTable[key]
    return totalCount


def probabilityTableFromCountTable(countTable):
    totalCount = totalCountFromCountTable(countTable)
    probabilityTable = dict()
    for key in countTable:
        probabilityTable[key] = countTable[key] / float(totalCount)
    return probabilityTable


def tokensProbabilityTableFromHitAndMisProbabilityTable(hitProbabilityTable, misProbabilityTable):
    probabilityTable = dict()
    for key in hitProbabilityTable:
        if key in misProbabilityTable:
            probabilityTable[key] = hitProbabilityTable[key] / (hitProbabilityTable[key] + misProbabilityTable[key])
        else:
            probabilityTable[key] = 1

    for key in misProbabilityTable:
        if not key in hitProbabilityTable:
            probabilityTable[key] = 0
    return probabilityTable


def probabilityListFromTokensAndTokensProbabilityTable(tokens, tokensProbabilityTable):
    probabilityList = list()
    for token in tokens:
        if token in tokensProbabilityTable:
            probabilityList.append(tokensProbabilityTable[token])
    return probabilityList


def eventProbabilityFromStringAndTokensProbabilityTable(string, tokensProbabilityTable):
    tokens = tokensFromString(string)
    probabilityList = probabilityListFromTokensAndTokensProbabilityTable(tokens, tokensProbabilityTable)
    A = 1
    B = 1
    for probability in probabilityList:
        A *= probability
        B *= (1 - probability)
    if A + B == 0:
        return 0
    else:
        return A / (A + B)


def tokensProbabilityTableFromHitAndMisStringList(hitStringList, misStringList):
    hitCountTable = dict()
    for hitString in hitStringList:
        addTokensToCountTable(tokensFromString(hitString), hitCountTable)
    hitProbabilityTable = probabilityTableFromCountTable(hitCountTable)

    misCountTable = dict()
    for misString in misStringList:
        addTokensToCountTable(tokensFromString(misString), misCountTable)
    misProbabilityTable = probabilityTableFromCountTable(misCountTable)

    tokensProbabilityTable = tokensProbabilityTableFromHitAndMisProbabilityTable(hitProbabilityTable, misProbabilityTable)

    return tokensProbabilityTable


def writeListToFileWithFileName(list, fileName):
    file = open(fileName, "w")
    for item in list:
        file.write("%s\n" % item)


def readListFromFileWithFileName(fileName):
    newList = list()
    file = open(fileName, "r")
    for line in file:
        newList.append(line.strip())
    return newList


hitFileName = "hitFileName.txt"
misFileName = "misFileName.txt"
testFileName = "testFileName.txt"

hitStringList = readListFromFileWithFileName(hitFileName)
misStringList = readListFromFileWithFileName(misFileName)
testStringList = readListFromFileWithFileName(testFileName)

tokensProbabilityTable = tokensProbabilityTableFromHitAndMisStringList(hitStringList, misStringList)


print "System Test"
for item in testStringList:
    probability = eventProbabilityFromStringAndTokensProbabilityTable(item, tokensProbabilityTable)
    print "probability =", probability
    print "weibo = ", item
    print "=============="


weibo = raw_input("Enter a weibo or 'quit': ")
while weibo != "quit":
    probability = eventProbabilityFromStringAndTokensProbabilityTable(weibo, tokensProbabilityTable)
    print "probability =", probability
    check = raw_input("Is it lottery weibo? (y/n/pass): ")
    if check == "y":
        hitStringList.append(weibo.strip())
    elif check == "n":
        misStringList.append(weibo.strip())
    print "============="
    weibo = raw_input("Enter a weibo or 'quit': ")

writeListToFileWithFileName(hitStringList, hitFileName)
writeListToFileWithFileName(misStringList, misFileName)
print "Saved user selections. Exit."
