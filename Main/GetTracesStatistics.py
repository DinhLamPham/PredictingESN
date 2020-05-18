from ChartHelper.BarChart import DataFrameToBarChart, TraceInfoToBarChart
from ChartHelper.PieChart import DataFrameToPieChart
from LogHelper.ReadFile import LogFileToTraceList
from MySQLHelper import Query
from CommonHelper.GVar import *
from CommonHelper.Common import *
from ChartHelper import BarChart
from CommonHelper import GVar
from MySQLHelper.Query import GetCellValue, UpdateFinishFuntionInDB, tblToDataFrame
import pandas as pd
import datetime

if platform.system() == 'Darwin':  # Mac OS
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

funcId = GetFileName(__file__)
parameterFrame = GetCellValue('parameter', tblFunctionList, ['id'], [funcId])
para = parameterFrame[0].splitlines()

_keySeparateInside = '!!'
tblName = para[0].split(_keySeparateInside)[-1]
viewType = para[1].split(_keySeparateInside)[-1]
showAct, showPer, showDuration = True, True, True

showAct = (viewType.find('Activity') >= 0)
showPer = (viewType.find('Performer') >= 0)
showDuration = (viewType.find('Duration') >= 0)



df = tblToDataFrame(tblName)
for i in range(0, len(df['Duration'])):
    df['Duration'][i] = MyTime_In_String_To_Number(df['Duration'][i], 'H')

outPutFile1, outPutFile2 = "currentTracesInfo_barchart.png", "currentTracesInfo_PieChart.png"

fullFilePath1 = str(Path(os.getcwd()).parent.parent) + GetGetTracesStatisticsFolder() + outPutFile1
fullFilePath2 = str(Path(os.getcwd()).parent.parent) + GetGetTracesStatisticsFolder() + outPutFile2
TraceInfoToBarChart(df, fullFilePath1, showAct, showPer, showDuration)

UpdateFinishFuntionInDB(funcId, outPutFile1)

print("Finished!")
