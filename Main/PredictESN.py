import sys
from pathlib import Path

from CommonHelper import GVar
from CommonHelper.Common import GetFileName, GetTrainedModelFolder, LoadFileToDict, GetPredictESNFolder
from CommonHelper.GVar import tblFunctionList, tblModel
from keras.models import load_model

from LogHelper.ReadFile import LogFileToTraceList
from LogHelper.SavePredictESN import SavePredictESNFile
from LogHelper.Trace import IntListToTraceSequence, RawTraceToActPer, ActPerToRawTrace
from MachineLearningHelper.trainningHelper import lstm_get_data_from_trace, one_hot_decode, \
    multi_decode_with_probability, encode_trace_sequence, multi_decode_with_top_rank
from Main.PredictPerWithAct import LoadModel, PredictPer
from MySQLHelper import Query
from MySQLHelper.Query import GetCellValue, UpdateFinishFuntionInDB
import platform
import os

countTryingFailed, totalResult = 0, 0
resulTraceWithActList, resulTraceWithPerList, resulTraceWithTimeList = [], [], []




def PredictActWithPro_Rank(_model, _inputSeq, _stepIn,
                           _name_to_int_set, _int_to_name_set, _predictMethod, _predictMethodVal, _maxStep):
    global countTryingFailed, totalResult, resulTraceWithActList

    if _inputSeq[-1] == "END":
        totalResult += 1
        print(
            "-------------------------------------------------------------------- Generated trace: %d" % totalResult, )
        resulTraceWithActList.append(_inputSeq)


    else:
        if len(_inputSeq) >= _maxStep:
            countTryingFailed += 1
            print("---------------------------------Can not reach END actvity.Try: ", countTryingFailed)
        else:
            if len(_inputSeq) >= stepIn:
                currentInput = _inputSeq[-_stepIn:]
                this_X = encode_trace_sequence(currentInput, _name_to_int_set)

                this_yHat = _model.predict(this_X, batch_size=1, verbose=0)
                original_this_X = IntListToTraceSequence(one_hot_decode(this_X.reshape(stepIn * feature, -1)),
                                                         _int_to_name_set)
                if _predictMethod == "Probability":
                    this_yHat_decoded = multi_decode_with_probability(this_yHat, _predictMethodVal)
                else:
                    this_yHat_decoded = multi_decode_with_top_rank(this_yHat, _predictMethodVal)

                potential_List_yhat = IntListToTraceSequence(this_yHat_decoded, _int_to_name_set)

                for y in potential_List_yhat.copy():
                    new_Seq = _inputSeq.copy()
                    new_Seq.append(y)
                    PredictActWithPro_Rank(_model, new_Seq, _stepIn,
                                           _name_to_int_set, _int_to_name_set, _predictMethod, _predictMethodVal, _maxStep)


if platform.system() == 'Darwin':  # Mac OS
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
funcId = GetFileName(__file__)

parameterFrame = GetCellValue('parameter', tblFunctionList, ['id'], [funcId])
para = parameterFrame[0].splitlines()

_keySeparateInside = '!!'
logFile = para[0].split(_keySeparateInside)[-1]
stepIn = (para[1].split(_keySeparateInside)[-1])
maxStep = int(para[2].split(_keySeparateInside)[-1])
predictMethod = (para[3].split(_keySeparateInside)[-1])
predictMethodValue = float(para[4].split(_keySeparateInside)[-1])
fileName = (para[5].split(_keySeparateInside)[-1])
fullFilePath = str(Path(os.getcwd()).parent.parent) + GetPredictESNFolder() + fileName

_keyWordSeparate, _keySeparateInside, _traceList = LogFileToTraceList(fullFilePath)
outputParameterValue = "Trained model does not exist!"
predictType, stepOut, feature = "Activity", "1", "1"
resultdf = GetCellValue('id', tblModel, ['name', 'stepin', 'stepout', 'predicttype', 'feature'],
                        [logFile, stepIn, stepOut, predictType, feature])

if len(resultdf) == 0:
    print(outputParameterValue)
else:
    modelName = resultdf[0]
    folderPath = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFile)
    modelFile = folderPath + modelName
    if not os.path.exists(modelFile):
        print(outputParameterValue)
    else:
        # Load model
        saved_model = load_model(modelFile)
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

        stepIn, stepOut, feature = int(stepIn), int(stepOut), int(feature)
        subTrace, subActTrace, subPerTrace, combineTrace, inputTest = [], [], [], None, None

        # Remove redundant input trace. (similar trace will be removed and not be used)
        listOfInputAct = []
        listOfInputPer = []
        dictMapActPer = {}
        for inputTrace in _traceList:
            currentInputAct = RawTraceToActPer(inputTrace, _keySeparateInside, 0)
            currentInputPer = RawTraceToActPer(inputTrace, _keySeparateInside, 1)
            dictMapActPer["!@#".join(currentInputAct)] = "!@#".join(currentInputPer)
            if not (currentInputAct in listOfInputAct):
                listOfInputAct.append(currentInputAct)
        if predictMethod == "Probability":
            predictMethodValue = predictMethodValue / 100
            for traceWithAct in listOfInputAct:
                PredictActWithPro_Rank(saved_model, traceWithAct, stepIn,
                                       name_to_int_set, int_to_name_set, predictMethod, predictMethodValue, maxStep)
        elif predictMethod == "TopRank":
            for traceWithAct in listOfInputAct:
                predictMethodValue = int(predictMethodValue)
                PredictActWithPro_Rank(saved_model, traceWithAct, stepIn,
                                       name_to_int_set, int_to_name_set, predictMethod, predictMethodValue, maxStep)


        # ResultList[]: Only contains actvity. => Predict Performer.
        # Load saved model of 1F_Act_Per
        print("Loading saved model...")
        saved_1F_Act_Per_Model, name_to_int_1F, int_to_name_1F = LoadModel(logFile, stepIn)
        if saved_1F_Act_Per_Model is not None:
            print(saved_1F_Act_Per_Model.summary())

        countPredictPer = 0
        for currentActList in resulTraceWithActList:
            if len(currentActList) <= stepIn:
                continue
            countPredictPer += 1
            print(
                "-------Predicting performer for generated trace %d/%d" % (countPredictPer, len(resulTraceWithActList)))
            thisPerList, thisTimeList = [], []
            currentOriginActInput = currentActList[:stepIn]
            thisPerList = dictMapActPer["!@#".join(currentOriginActInput)].split("!@#")

            #  PredictPer(logFile, _saveModel, actList, stepIn, name_to_int_set, int_to_name_set, perList):
            if saved_1F_Act_Per_Model is not None:
                thisPerList = PredictPer(saved_1F_Act_Per_Model, currentActList,
                                     stepIn, name_to_int_1F, int_to_name_1F, thisPerList)
            else:
                [thisPerList.append("CommingSoon") for _ in range(stepIn, len(currentActList))]


            [thisTimeList.append("NULL") for _ in range(len(currentActList))]

            resulTraceWithPerList.append(thisPerList)
            resulTraceWithTimeList.append(thisTimeList)

        finalResult = []
        # [finalResult.append(act+_keySeparateInside+per+_keySeparateInside+"NULL")
        #  for act, per in zip(resulTraceWithActList, resulTraceWithPerList)]
        for actList, perList, timeList in zip(resulTraceWithActList, resulTraceWithPerList, resulTraceWithTimeList):
            finalResult.append(ActPerToRawTrace(actList, perList, timeList, _keySeparateInside))

        outputFileName = logFile.replace('.txt', '') + "_stepIn_" + str(stepIn) + "_" + str(predictMethodValue) +"_percent.txt"
        outputParameterValue = outputFileName
        SavePredictESNFile(outputFileName, _keyWordSeparate, _keySeparateInside, finalResult)

# Update database
UpdateFinishFuntionInDB(funcId, outputParameterValue)
print("finished!")
sys.exit()
