from pathlib import Path

from CommonHelper import GVar
from CommonHelper.Common import GetFileName, GetTrainedModelFolder, LoadFileToDict, GetPredictESNFolder
from CommonHelper.GVar import tblFunctionList, tblModel
from keras.models import load_model

from LogHelper.ReadFile import LogFileToTraceList
from LogHelper.SavePredictESN import SavePredictESNFile
from LogHelper.Trace import IntListToTraceSequence
from MachineLearningHelper.trainningHelper import lstm_get_data_from_trace, one_hot_decode
from MySQLHelper import Query
from MySQLHelper.Query import GetCellValue, SelectTableWithCondition, UpdateFinishFuntionInDB
import platform
import os


def RawTraceToCombine(_inputTrace, _keySeparateInside):
    actList, perList = [], []
    for event in _inputTrace:
        currentAct, currentPer = event.split(_keySeparateInside)[0], event.split(_keySeparateInside)[1]
        actList.append(currentAct)
        perList.append(currentPer)

    [actList.append("END") for _ in range(stepOut)]
    [perList.append("END") for _ in range(stepOut)]
    result = GVar.CombineTrace(actList, perList)
    return result


# def UpdateDB(_output):
#     _tblName = GVar.tblFunctionList
#     _headerCondition = 'id'
#     _valueCondition = funcId
#     _headerUpdate = ['output', 'run']
#     _valueUpdate = [_output, 'finished']
#     Query.UpdateTable(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate)


def GetLogIdWithMaxVal_Accuracy(inputDf):
    maxVal = max(inputDf['val_accuracy'][:])
    for logId, stepin, stepout, val_acc in zip(inputDf['id'][:], inputDf['stepin'][:],
                                               inputDf['stepout'][:], inputDf['val_accuracy'][:]):
        if val_acc == maxVal:
            return logId, stepin, stepout


if platform.system() == 'Darwin':  # Mac OS
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

funcId = GetFileName(__file__)

parameterFrame = GetCellValue('parameter', tblFunctionList, ['id'], [funcId])
para = parameterFrame[0].splitlines()

_keySeparateInside = '!!'
logFile = para[0].split(_keySeparateInside)[-1]
predictType = (para[1].split(_keySeparateInside)[-1])
stepIn = (para[2].split(_keySeparateInside)[-1])
stepOut = (para[3].split(_keySeparateInside)[-1])
feature = para[4].split(_keySeparateInside)[-1]
maxStepCount = int(para[5].split(_keySeparateInside)[-1]) - int(stepIn)
fileName = (para[6].split(_keySeparateInside)[-1])
fullFilePath = str(Path(os.getcwd()).parent.parent) + GetPredictESNFolder() + fileName

_keyWordSeparate, _keySeparateInside, _traceList = LogFileToTraceList(fullFilePath)

outputParameterValue = "Trained model does not exist!"

resultdf = SelectTableWithCondition(['id', 'predictType', 'feature', 'stepin', 'stepout', 'val_accuracy'], tblModel,
                                    ['name', 'predicttype', 'stepin', 'stepout', 'feature'],
                                    [logFile, predictType, str(stepIn), str(stepOut), feature])

if len(resultdf) == 0:
    print(outputParameterValue)
else:
    # Select trained model with the best val_accuracy
    modelName, stepIn, stepOut = GetLogIdWithMaxVal_Accuracy(resultdf)
    folderPath = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFile)
    name_to_int_set = LoadFileToDict(folderPath + GetCellValue('name_to_int_set', tblModel,
                                                               ['name', 'stepin', 'stepout', 'predicttype', 'feature'],
                                                               [logFile, str(stepIn), str(stepOut), predictType,
                                                                feature])[0])

    int_to_name_set = LoadFileToDict(folderPath + GetCellValue('int_to_name_set', tblModel,
                                                               ['name', 'stepin', 'stepout', 'predicttype', 'feature'],
                                                               [logFile, str(stepIn), str(stepOut), predictType,
                                                                feature])[0])
    modelFile = folderPath + modelName
    if not os.path.exists(modelFile):
        print(outputParameterValue)
    else:
        # Load model
        my_saved_model = load_model(modelFile)
        print("Model file: ", modelName, my_saved_model.summary())

        stepIn, stepOut, feature = int(stepIn), int(stepOut), int(feature)
        timepredict = "NULL"
        outputTraceList = []
        countTrace = 0
        for trace in _traceList:
            countTrace += 1
            print("Calculating for trace %d/%d" % (countTrace, len(_traceList)))
            currentTraceOutput = trace
            countTotalStep = 0
            while countTotalStep < maxStepCount:
                lastStepInValue = currentTraceOutput[-stepIn:]
                if lastStepInValue[-1].split(_keySeparateInside)[0] == "END" or \
                        lastStepInValue[-1].split(_keySeparateInside)[1] == "END":
                    print("end activity reached!")
                    break
                currentStepInput = RawTraceToCombine(lastStepInValue, _keySeparateInside)
                # Convert InputList -> Vector of
                subX, _ = lstm_get_data_from_trace(currentStepInput, predictType, feature, name_to_int_set, stepIn, stepOut)
                subyhat = my_saved_model.predict(subX, batch_size=1, verbose=0)

                # original_subX = IntListToTraceSequence(one_hot_decode(subX.reshape(stepIn * feature, -1)), int_to_name_set)
                original_subyhat = IntListToTraceSequence(one_hot_decode(subyhat.reshape(stepOut * feature, -1)), int_to_name_set)
                resultAct, resultPer = original_subyhat[:stepOut], original_subyhat[stepOut:]
                combineResult = [(x + _keySeparateInside + y + _keySeparateInside + timepredict) for x, y in
                                 zip(resultAct, resultPer)]

                [currentTraceOutput.append(x) for x in combineResult]
                countTotalStep += 1
            outputTraceList.append(currentTraceOutput)

        outputFileName = logFile.replace('.txt', '') + "__result.txt"
        outputParameterValue = outputFileName
        SavePredictESNFile(outputFileName, _keyWordSeparate, _keySeparateInside, outputTraceList)

# Update database
UpdateFinishFuntionInDB(funcId, outputParameterValue)
print("Finish predict ESN!")
