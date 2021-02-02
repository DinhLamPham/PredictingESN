from pathlib import Path

from CommonHelper import GVar
from CommonHelper.Common import GetFileName, GetTrainedModelFolder, LoadFileToDict, GetPredictESNFolder
from CommonHelper.GVar import tblFunctionList, tblModel
from keras.models import load_model

from LogHelper.ReadFile import LogFileToTraceList
from LogHelper.SavePredictESN import SavePredictESNFile
from LogHelper.Trace import IntListToTraceSequence, RawTraceToActPer, ActPerToRawTrace
from MachineLearningHelper.trainningHelper import lstm_get_data_from_trace, one_hot_decode, \
    multi_decode_with_probability, encode_trace_sequence
from MySQLHelper import Query
from MySQLHelper.Query import GetCellValue, UpdateFinishFuntionInDB
import platform
import os


def LoadModel(logFile, stepIn):
    _keySeparateInside = '!!'
    folderPath = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFile)
    output = "Trained model does not exist!"
    stepOut = "1"
    predictType = "1F_Activity_Performer"
    feature = "1.5"
    resultdf = GetCellValue('id', tblModel, ['name', 'stepin', 'stepout', 'predicttype', 'feature'],
                            [logFile, str(stepIn), stepOut, predictType, feature])

    if len(resultdf) == 0:
        print(output)
        return None, None, None

    name_to_int_set = LoadFileToDict(
        folderPath + GetCellValue('name_to_int_set', tblModel,
                                  ['name', 'stepin', 'stepout',
                                   'predicttype', 'feature'],
                                  [logFile, str(stepIn), stepOut, predictType,
                                   feature])[0])

    int_to_name_set = LoadFileToDict(
        folderPath + GetCellValue('int_to_name_set', tblModel,
                                  ['name', 'stepin', 'stepout',
                                   'predicttype', 'feature'],
                                  [logFile, str(stepIn), stepOut, predictType,
                                   feature])[0])

    modelName = resultdf[0]
    folderPath = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFile)
    _saveModel = load_model(folderPath + modelName)
    return _saveModel, name_to_int_set, int_to_name_set


def PredictPer(_saveModel, actList, stepIn, name_to_int_set, int_to_name_set, perList):
    feature, stepOut, predictType = "1.5", "1", "Performer"
    stepIn, stepOut, feature = int(stepIn), int(stepOut), float(feature)

    [perList.append("END") for _ in range(stepIn, len(actList))]
    combineTrace = GVar.CombineTrace(actList, perList)

    subX, _ = lstm_get_data_from_trace(combineTrace, predictType, feature, name_to_int_set, stepIn, stepOut)
    subyhat = _saveModel.predict(subX, batch_size=1, verbose=1)


    subyhat_decoded = one_hot_decode(subyhat)
    original_subyhat = IntListToTraceSequence(subyhat_decoded, int_to_name_set)
    perList = perList[:stepIn]
    [perList.append(y) for y in original_subyhat[1:]]

    return perList


