import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd


def ExcelFilesToBoxPlot(_logFolder, _trainedTypeFolder):
    trainedPath = os.path.join(os.path.dirname(os.getcwd()), "TrainedModel", _logFolder, _trainedTypeFolder)
    listFile = sorted(os.listdir(trainedPath))

    result = pd.DataFrame()
    ouputFile = ''
    for file in listFile:
        if not (('.xlsx' in file) and (_logFolder in file)):
            continue
        colName = file.split('.xlsx')[0][-3:]
        ouputFile = os.path.join(trainedPath, file.split('.xlsx')[0][:-3])
        df = pd.read_excel(os.path.join(trainedPath, file))
        col_Val = df[df.columns[0]]
        result[colName] = col_Val
        print(result)

    data = pd.melt(result)
    data.dropna(inplace=True)
    DataFrameToBoxPlot(data, ouputFile)


def DataFrameToBoxPlot(_inputDf, _outputFile):
    bplot = sns.boxplot(x="variable", y="value", data=_inputDf, width=0.3, palette="Set2")

    bplot.set_xlabel(r"StepInput_StepOutput ($\eta_i\_\eta_o$)", fontsize=10)
    bplot.set_ylabel("Training accuracy", fontsize=10)
    bplot.tick_params(labelsize=8)
    # plt.savefig(_outputFile, bbox_inches='tight')
    # print('Saved file: ', _outputFile)
    plt.show()


list_type = ['1F_A', '2F_A']
listLog = ['1_InternationalDeclarations']

for log in listLog:
    for _type in list_type:
        plt.clf()
        ExcelFilesToBoxPlot(log, _type)

sys.exit()
print("finished")
