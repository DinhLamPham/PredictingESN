import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from keras.models import load_model
from CommonHelper import GVar
from CommonHelper.Common import LoadFileToDict
from CommonHelper.GVar import CombineTrace
from LogHelper.ReadFile import ReadSavedLog
from LogHelper.Trace import IntListToTraceSequence
from MachineLearningHelper.trainningHelper import lstm_get_data_from_trace, one_hot_decode, prepare_os_environment

prepare_os_environment()


def LoadModelAndParams(_logFolder, _trainedTypeFolder):
    trainedPath = os.path.join(os.path.dirname(os.getcwd()), "TrainedModel", _logFolder, _trainedTypeFolder)
    listFile = sorted(os.listdir(trainedPath))

    ouputFile = ''
    resultDf = pd.DataFrame()
    modelCol, evaluatedVal = [], []
    for file in listFile:
        if not ('.h5' in file):
            continue
        fileName = file.split('.')[0]
        stepIn = fileName[-3:].split('_')[0]
        stepOut = fileName[-3:].split('_')[-1]
        predictType = fileName[:-3].split('_')[-1]
        feature = _trainedTypeFolder[0]
        ouputFile = os.path.join(trainedPath, _trainedTypeFolder + '_validation.xlsx')

        modelFile = os.path.join(trainedPath, file)
        name_to_int_Path = os.path.join(trainedPath, _logFolder + '_predict_%s_%sfeature_NameToInt.pickle' % (predictType, feature))
        int_to_name_Path = os.path.join(trainedPath,
                                        _logFolder + '_predict_%s_%sfeature_IntToName.pickle' % (predictType, feature))
        saved_model = load_model(modelFile)
        name_to_int_set = LoadFileToDict(name_to_int_Path)
        int_to_name_set = LoadFileToDict(int_to_name_Path)
        currentEvaluateVal = EvaluateModel(_logFolder, feature, predictType, stepIn, stepOut, name_to_int_set, int_to_name_set, saved_model)
        modelCol.append(stepIn + '_' + stepOut)
        evaluatedVal.append(currentEvaluateVal)
    resultDf[_trainedTypeFolder] = modelCol
    resultDf['Validation Value'] = evaluatedVal
    resultDf.to_excel(ouputFile, index=False)



def EvaluateModel(_logFile, _feature, _predictType, _n_in, _n_out, _name_to_int_set, _int_to_name_set, _model):

    train_log, test_log, train_combineLog, test_combineLog = None, None, None, None
    inputTrain, inputTest = None, None

    logSize = len(GVar.traceWithEventList)
    split_point = int(logSize * 0.7)
    # Select dictionary
    test_log, test_combineLog = None, None
    inputTrain, inputTest = None, None
    # Select dictionary
    lenTest = 0
    if _feature == '1':
        if _predictType == "Activity":
            test_log = GVar.traceWithActList[split_point:]

        if _predictType == "Performer":
            test_log = GVar.traceWithPerList[split_point:]

        inputTest = test_log
        lenTest = len(test_log)

    if _feature == '2':
        test_combineLog = CombineTrace(GVar.traceWithActList[split_point:], GVar.traceWithPerList[split_point:])
        inputTest = test_combineLog
        lenTest = len(test_combineLog.getAllTraceWithAct())

    globalAverage = []
    for i in range(lenTest):
        if _feature == '1':
            trace = inputTest[i]
            traceLen = len(trace)
        if _feature == '2':
            trace = inputTest.get_Trace_I_With_Combine(i)
            traceLen = inputTest.get_Trace_Length(i)

        if traceLen < (int(_n_in) + int(_n_out)):
            continue
        X, y = lstm_get_data_from_trace(trace, _predictType, int(_feature), _name_to_int_set, int(_n_in), int(_n_out))
        yhat = _model.predict(X, batch_size=GVar.batch_size, verbose=0)

        #     # decode all pairs
        percent = [1 if one_hot_decode(y[i]) == one_hot_decode(yhat[i]) else 0 for i in range(len(X))]
        currentAverage = sum(percent) / len(X)
        globalAverage.append(currentAverage)
        print(_logFile, "------Validation in trace %d/%d, %sFeature_%s ----- stepIn: %s, stepOut: %s: "
              % (i, lenTest, _feature, _predictType, _n_in, _n_out), currentAverage)
    thisModelAvaluateValue = sum(globalAverage)/len(globalAverage)
    print("Global average: ", thisModelAvaluateValue)
    return thisModelAvaluateValue


list_type = ['1F_A', '1F_P', '2F_A', '2F_P']
listLog = ['5_BPIC15_1', '6_BPIC15_2']

for log in listLog:
    ReadSavedLog(log + '.txt')
    for _type in list_type:
        LoadModelAndParams(log, _type)

sys.exit()
print("finished")
