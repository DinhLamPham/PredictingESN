from pathlib import Path

from CommonHelper import GVar
from CommonHelper.Common import GetFileName, GetTrainedModelFolder, LoadFileToDict
from CommonHelper.GVar import tblFunctionList, tblModel
from keras.models import load_model
from LogHelper.Trace import IntListToTraceSequence
from MachineLearningHelper.trainningHelper import lstm_get_data_from_trace, one_hot_decode
from MySQLHelper import Query
from MySQLHelper.Query import GetCellValue, UpdateFinishFuntionInDB
import platform
import os


if platform.system() == 'Darwin':  # Mac OS
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

funcId = GetFileName(__file__)

parameterFrame = GetCellValue('parameter', tblFunctionList, ['id'], [funcId])
para = parameterFrame[0].splitlines()

_keySeparateInside = '!!'
logFile = para[0].split(_keySeparateInside)[-1]
stepIn = (para[1].split(_keySeparateInside)[-1])
stepOut = (para[2].split(_keySeparateInside)[-1])
predictType = para[3].split(_keySeparateInside)[-1]
feature = para[4].split(_keySeparateInside)[-1]
output = "Trained model does not exist!"

resultdf = GetCellValue('id', tblModel, ['name', 'stepin', 'stepout', 'predicttype', 'feature'],
                        [logFile, stepIn, stepOut, predictType, feature])
if len(resultdf) == 0:
    print(output)
else:
    modelName = resultdf[0]
    folderPath = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFile)
    name_to_int_set = LoadFileToDict(
        folderPath + GetCellValue('name_to_int_set', tblModel,
                                                                               ['name', 'stepin', 'stepout',
                                                                                'predicttype', 'feature'],
                                                                               [logFile, stepIn, stepOut, predictType,
                                                                                feature])[0])

    int_to_name_set = LoadFileToDict(
        folderPath + GetCellValue('int_to_name_set', tblModel,
                                                                               ['name', 'stepin', 'stepout',
                                                                                'predicttype', 'feature'],
                                                                               [logFile, stepIn, stepOut, predictType,
                                                                                feature])[0])

    modelFile = folderPath + modelName

    if not os.path.exists(modelFile):
        print(output)
    else:
        # Load model
        saved_model = load_model(modelFile)

        stepIn, stepOut, feature = int(stepIn), int(stepOut), int(feature)
        subTrace, subActTrace, subPerTrace, combineTrace, inputTest = [], [], [], None, None
        if feature == 1:
            for i in range(5, 5 + stepIn):
                subTrace.append(para[i].split(_keySeparateInside)[-1])
            [subTrace.append("END") for _ in range(stepOut)]
            inputTest = subTrace

        if feature == 2:
            for i in range(5, 5 + stepIn):
                subActTrace.append(para[i].split(_keySeparateInside)[-1].split(GVar.keySeparateInside)[0])
                subPerTrace.append(para[i].split(_keySeparateInside)[-1].split(GVar.keySeparateInside)[-1])
            [subActTrace.append("END") for _ in range(stepOut)]
            [subPerTrace.append("END") for _ in range(stepOut)]
            combineTrace = GVar.CombineTrace(subActTrace, subPerTrace)
            inputTest = combineTrace

        print("Model file: ", modelName)
        # Convert InputList -> Vector of
        subX, _ = lstm_get_data_from_trace(inputTest, predictType, feature, name_to_int_set, stepIn, stepOut)
        subyhat = saved_model.predict(subX, batch_size=1, verbose=1)
        print(subyhat)

        original_subX = IntListToTraceSequence(one_hot_decode(subX.reshape(stepIn * feature, -1)), int_to_name_set)


        if predictType == "Activity_Performer":
            original_subyhat = IntListToTraceSequence(one_hot_decode(subyhat.reshape(stepOut * 2, -1)), int_to_name_set)
            resultAct, resultPer = original_subyhat[:stepOut], original_subyhat[stepOut:]
            combineResult = [x + GVar.keySeparateInside + y for x, y in zip(resultAct, resultPer)]
            output = GVar.keyWordSeparate.join(combineResult)

        if predictType == "Activity" or predictType == "Performer": # predictype == "Activity" / "Performer"
            subyhat = subyhat.reshape(stepOut * 1, -1)
            subyhat_decoded = one_hot_decode(subyhat)
            original_subyhat = IntListToTraceSequence(subyhat_decoded, int_to_name_set)
            output = GVar.keyWordSeparate.join(original_subyhat)

        print('Input:', original_subX)
        print('Predicted:', original_subyhat)

# Update database
UpdateFinishFuntionInDB(funcId, output)
