import numpy as np
from collections import Counter
from CommonHelper.GVar import *
from CommonHelper import GVar
from LogHelper.Trace import TraceSequenceToIntList, IntListToTraceSequence


# Read from log and return _keyWordSeparate, _keySeparateInside, TraceList[]
def LogFileToTraceList(_filePath):
    _keyWordSeparate, _keySeparateInside = '', ''
    _traceList = []
    with open(_filePath, encoding='utf-8') as f:
        _keyWordSeparate = f.readline().strip()
        _keySeparateInside = f.readline().strip()
        while True:
            currentLine = f.readline()
            if not currentLine:
                break
            currentTrace = currentLine.strip().split(GVar.keyWordSeparate)
            _traceList.append(currentTrace)
    return _keyWordSeparate, _keySeparateInside, _traceList



# Read Log in List<String> format -> traceWithEventList[], traceWithActList[], traceWithPerList[], some SET{},...
def ReadSavedLog(_file):
    GVar.actSet, GVar.perSet, GVar.combineSet = {'START', 'END'}, {'START', 'END'}, {'START', 'END'}
    with open(_file, encoding='utf-8') as f:
        GVar.keyWordSeparate = f.readline().strip()
        GVar.keySeparateInside = f.readline().strip()
        while True:
            currentLine = f.readline()
            if not currentLine:
                break
            currentTrace = currentLine.strip().split(GVar.keyWordSeparate)
            GVar.traceWithEventList.append(currentTrace)

            if GVar.maxLen < len(currentTrace):
                GVar.maxLen = len(currentTrace)

            currentTraceWithAct, currentTraceWithPer = [], []
            for event in currentTrace:
                currentAct = event.split(GVar.keySeparateInside)[GVar.posOfAct]
                currentPer = event.split(GVar.keySeparateInside)[GVar.postOfPer]

                GVar.actSet.add(currentAct)
                GVar.perSet.add(currentPer)

                currentTraceWithAct.append(currentAct)
                currentTraceWithPer.append(currentPer)

            GVar.traceWithActList.append(currentTraceWithAct)
            GVar.traceWithPerList.append(currentTraceWithPer)

    GVar.combineSet = GVar.actSet.copy()
    GVar.combineSet.update(GVar.perSet)

    GVar.actSet, GVar.perSet, GVar.combineSet = sorted(GVar.actSet), sorted(GVar.perSet), sorted(GVar.combineSet)
    GVar.int_to_act = {k: w for k, w in enumerate(GVar.actSet)}
    GVar.act_to_int = {w: k for k, w in GVar.int_to_act.items()}

    GVar.int_to_per = {k: w for k, w in enumerate(GVar.perSet)}
    GVar.per_to_int = {w: k for k, w in GVar.int_to_per.items()}

    GVar.int_to_combine = {k: w for k, w in enumerate(GVar.combineSet)}
    GVar.combine_to_int = {w: k for k, w in GVar.int_to_combine.items()}
#
# int_trace_act_0 = TraceSequenceToIntList(GlobalVariables.traceWithActList[5], GlobalVariables.act_to_int)
# int_trace_per_0 = TraceSequenceToIntList(GlobalVariables.traceWithPerList[5], GlobalVariables.per_to_int)
#
# name_trace_act_0 = IntListToTraceSequence(int_trace_act_0, GlobalVariables.int_to_act)

