# ['act1', 'act2', 'act3', 'act4', 'act5'] -> ['1', '2', '3', '4', '5']
from CommonHelper import GVar

def TraceSequenceToIntList_WithoutAppend(_currentTrace, name_to_int_Set):
    int_trace = []
    for x in _currentTrace:
        alias = name_to_int_Set[x]
        int_trace.append(alias)
    return int_trace


def TraceSequenceToIntList(_currentTrace, name_to_int_Set):
    int_trace = []
    for x in _currentTrace:
        alias = name_to_int_Set[x]
        int_trace.append(alias)

    # append end process until the size equal to _maxlen
    for _ in range(GVar.n_out):
        int_trace.append(name_to_int_Set["END"])
    for _ in range(GVar.n_in):
        int_trace.insert(0, name_to_int_Set["START"])
    return int_trace


def IntListToTraceSequence(_intList, int_to_name_set):
    traceSequence = []
    for x in _intList:
        alias = int_to_name_set[x]
        traceSequence.append(alias)
    return traceSequence


def RawTraceToActPer(_inputTrace, _keySepareinside, _pos):
    result = []
    for event in _inputTrace:
        result.append(event.split(_keySepareinside)[_pos])
    return result


def ActPerToRawTrace(_actList, _perList, _timeList, _keySepareinside):
    result = []
    for act, per, time in zip(_actList, _perList, _timeList):
        result.append(act + _keySepareinside + per + _keySepareinside + time)
    return result


