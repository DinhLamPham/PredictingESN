from ChartHelper.BarChart import DataFrameToBarChart
from ChartHelper.PieChart import DataFrameToPieChart
from LogHelper.ReadFile import LogFileToTraceList
from MySQLHelper import Query
from CommonHelper.GVar import *
from CommonHelper.Common import *
from ChartHelper import BarChart
from CommonHelper import GVar
from MySQLHelper.Query import GetCellValue, UpdateFinishFuntionInDB
import pandas as pd
import datetime

if platform.system() == 'Darwin':  # Mac OS
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def GetDurationBetween(_startTime, _endTime):
    if _startTime == "NULL" or _endTime == "NULL" or _endTime == "END":
        return 0

    _startTime = iso_8601_format(_startTime)
    _endTime = iso_8601_format(_endTime)
    duration = _endTime - _startTime
    result = duration.total_seconds() / (60 * 60)
    return result


# def GetStatistic(_keyWordSeparate, _keySeparateInside, _traceList, _posOfAct, _posOfPer, _posOfTime):
    #
    # myDf = pd.DataFrame(data, columns=_columnList)
    # print("Calculating...")
    # countTrace = 0
    # for trace in _traceList:
    #     countTrace += 1
    #     print("....Trace %d/%d" % (countTrace, len(_traceList)))
    #     trace = trace[1:]
    #     currentKey = trace[0].split(_keySeparateInside)[_posToget]
    #     currentTime = trace[0].split(_keySeparateInside)[_posOfTime]
    #     for i in range(1, len(trace)):
    #         nextKey = trace[i].split(_keySeparateInside)[_posToget]
    #         nextTime = trace[i].split(_keySeparateInside)[_posOfTime]
    #         duration = GetDurationBetween(currentTime, nextTime)
    #         if currentKey in _columnList:
    #             myDf[currentKey][0] = myDf[currentKey][0] + 1
    #             myDf[currentKey][1] = myDf[currentKey][1] + duration
    #
    #         currentKey = nextKey
    #         currentTime = nextTime
    # return myDf


funcId = GetFileName(__file__)
parameterFrame = GetCellValue('parameter', tblFunctionList, ['id'], [funcId])
para = parameterFrame[0].splitlines()

_keySeparateInside = '!!'
logFile = para[0].split(_keySeparateInside)[-1]
viewType = (para[1].split(_keySeparateInside)[-1])
posOfAct, posOfPer, posOfTime = 0, 1, 2

fullFilePath = str(Path(os.getcwd()).parent.parent) + GetGetTracesStatisticsFolder() + logFile
_keyWordSeparate, _keySeparateInside, _traceList = LogFileToTraceList(fullFilePath)
#
# df = GetStatistic(_keyWordSeparate, _keySeparateInside, _traceList, posToGet, posOfTime, members)
# outPutFile1, outPutFile2 = logFile + "_barchart.png", logFile + "_PieChart.png"
#
# fullFilePath1 = str(Path(os.getcwd()).parent.parent) + GetGetTracesStatisticsFolder() + outPutFile1
# fullFilePath2 = str(Path(os.getcwd()).parent.parent) + GetGetTracesStatisticsFolder() + outPutFile2
# DataFrameToBarChart(df, fullFilePath1, 0)
# DataFrameToPieChart(df, fullFilePath2, 0)
#
# UpdateFinishFuntionInDB(funcId, outPutFile1 + _keySeparateInside + outPutFile2)
UpdateFinishFuntionInDB(funcId, "empty!")
print("Finished!")
