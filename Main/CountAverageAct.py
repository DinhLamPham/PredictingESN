import pandas as pd

def GetAverageActivity(_file):

    with open(_file + '.txt', encoding='utf-8') as f:
        keyWordSeparate = f.readline().strip()
        keySeparateInside = f.readline().strip()
        traceLenList = []
        while True:
            currentLine = f.readline()
            if not currentLine:
                break
            currentTrace = currentLine.strip().split(keyWordSeparate)
            traceLenList.append(len(currentTrace))

    return sum(traceLenList)/len(traceLenList)


listLog = ['0 Helpdesk', '1 InternationalDeclarations', '2 BPI_Challenge_2012', '3 BPI Challenge 2017']
resultDf = pd.DataFrame()
for log in listLog:
    avg = [GetAverageActivity(log)]
    resultDf[log] = avg

print(resultDf)
resultDf.to_excel('Average activity summary.xlsx')