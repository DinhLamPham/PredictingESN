import os
from os.path import dirname, abspath
from pathlib import Path

from CommonHelper.Common import GetTrainedModelFolder

tblActivities = 'Activities'
tblPerformers = 'Performers'

outPutImageFolder = dirname(dirname(abspath(__file__))) + r'/OutputImage/'
tblFunctionList = 'FunctionList'
tblModel = 'model'
tblSelectingEvent = 'SelectingEvent'
tblFunctionResultHeader = ['id', 'name', 'parameter', 'describer', 'outputType', 'output', 'run', 'position']
tblModelHeader = ['id', 'name', 'stepin', 'stepout', 'predicttype', 'feature', 'name_to_int_set', 'int_to_name_set', 'val_accuracy']

funcNotyetStatus = 'notyet'
columnRunHeader = 'run'

# LOg.......
keyWordSeparate = "!@#"
keySeparateInside = "!!"
traceWithEventList = []
traceWithActList = []
traceWithPerList = []

posOfAct, postOfPer, postOfTime = 0, 1, 2
actSet, perSet, combineSet = {'START', 'END'}, {'START', 'END'}, {'START', 'END'}
maxLen = 0

int_to_act, act_to_int = {}, {}
int_to_per, per_to_int = {}, {}
int_to_combine, combine_to_int = {}, {}
name_to_int_FileName, int_to_name_FileName = "", ""

trainedFolder = "TrainedModel"
currentTrainingFile = r"0 Helpdesk.txt"
model_name = currentTrainingFile.replace(".txt", "")
# LSTM Parameter
maxRepeatStep = 0
n_in, n_out = 0, 0
encoded_length = 0
feature = 1
predicttype = "Activity"
batch_size = 1


predictESNFolder = "PredictESN"
GetTracesStatisticsFolder = "GetTracesStatistics"
#-----------------------


class CombineTrace:
    def __init__(self, _traceWithAct=[], _traceWithPer=[]):
        self.traceWithAct = _traceWithAct
        self.traceWithPer = _traceWithPer

    def getAllTraceWithAct(self):
        return self.traceWithAct

    def getAllTraceWithPer(self):
        return self.traceWithPer

    def get_Trace_I_With_Act(self, i=0):
        return self.traceWithAct[i]

    def get_Trace_I_With_Per(self, i=0):
        return self.traceWithPer[i]

    def get_Trace_I_With_Combine(self, i=0):
        return CombineTrace(self.get_Trace_I_With_Act(i), self.get_Trace_I_With_Per(i))

    def get_Trace_Length(self, i=0):
        return len(self.get_Trace_I_With_Act(i))


def Init_New_Log(listPara):
    _feature, _predicttype = listPara[0], listPara[1]
    global keyWordSeparate, keySeparateInside, traceWithEventList, traceWithActList, \
        traceWithPerList, actSet, perSet, maxLen, model_name, currentTrainingFile, \
        name_to_int_FileName, int_to_name_FileName, feature, combineSet, predicttype
    keyWordSeparate = ""
    keySeparateInside = ""
    traceWithEventList = []
    traceWithActList = []
    traceWithPerList = []
    feature = _feature
    predicttype = _predicttype
    actSet, perSet, combineSet = {'START', 'END'}, {'START', 'END'}, {'START', 'END'}
    maxLen = 0
    model_name = currentTrainingFile.replace(".txt", "")
    name_to_int_FileName = model_name + "_predict_" + predicttype + "_" + str(_feature) + "feature_" + "NameToInt.pickle"
    int_to_name_FileName = model_name + "_predict_" + predicttype + "_" + str(_feature) + "feature_" + "IntToName.pickle"


