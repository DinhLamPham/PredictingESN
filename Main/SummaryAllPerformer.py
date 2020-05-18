from MySQLHelper import Query
from CommonHelper.GVar import *
from CommonHelper.Common import *
from ChartHelper import BarChart
from CommonHelper import GVar


def main():
    df = Query.tblToDataFrame(tblPerformers)
    funcName = GetFileName(__file__)
    outputFile = GVar.outPutImageFolder + GetFileName(__file__) + '.png'
    columns = [1, 2]
    BarChart.DataFrameToBarChart(df, columns, outputFile)

    _tblName = tblFunctionList
    _headerCondition = 'id'
    _valueCondition = funcName
    _headerUpdate = ['output', 'run']
    _valueUpdate = [outputFile, 'finished']

    Query.UpdateTable(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate)


if __name__ == '__main__':
    main()
    print('finished')
