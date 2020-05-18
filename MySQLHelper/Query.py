from CommonHelper import GVar
from CommonHelper.GVar import tblFunctionList, columnRunHeader
from LogHelper.SaveTrainHistory import SaveSQLInsertTraindModel
from MySQLHelper import sqlSyntax, mySQLSettings
from MySQLHelper.mySQLSettings import *
from CommonHelper.Communicate import ErrorHandler

import pandas as pd


def UpdateFinishFuntionInDB(funcId, _output):
    _tblName = GVar.tblFunctionList
    _headerCondition = 'id'
    _valueCondition = funcId
    _headerUpdate = ['output', 'run']
    _valueUpdate = [_output, 'finished']
    UpdateTable(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate)


def SetFuntionIsRunning(_function, _status):
    _tblName = tblFunctionList
    _headerCondition = 'name'
    _valueCondition = _function
    _headerUpdate = ['run']
    _valueUpdate = [_status]
    UpdateTable(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate)


def tblToDataFrame(_tblName):
    sql = "SELECT * FROM " + _tblName
    connection = mySQLSettings.OpenConnection()
    return pd.read_sql(sql, connection)


def GetFunctionStatus(_status):
    sql = "SELECT * FROM " + tblFunctionList + " WHERE " + columnRunHeader + " ='" + _status + "'"
    connection = mySQLSettings.OpenConnection()
    df = pd.read_sql(sql, connection)
    result = zip(df['id'], df['run'])
    return result


# Get cell value in table and return in dataframe
def GetCellValue(_columnValue, _tblName, _columnCondition, _valueCondition):
    # condList = []
    # for x, y in zip(_columnCondition, _valueCondition):
    #     condList.append(x + "='" + y + "'")
    # mylist1 = ",".join(condList)

    condList = " and ".join([x + "='" + y + "'" for x, y in zip(_columnCondition, _valueCondition)])

    sql = "SELECT " + _columnValue + " FROM " + _tblName + " WHERE " + condList
    connection = mySQLSettings.OpenConnection()
    df = pd.read_sql(sql, connection)
    return df[_columnValue]


def SelectTableWithCondition(_columnValue, _tblName, _columnCondition, _valueCondition):
    # condList = []
    # for x, y in zip(_columnCondition, _valueCondition):
    #     condList.append(x + "='" + y + "'")
    # mylist1 = ",".join(condList)
    colList = ", ".join(_columnValue)
    condList = " and ".join([x + "='" + y + "'" for x, y in zip(_columnCondition, _valueCondition)])

    sql = "SELECT " + colList + " FROM " + _tblName + " WHERE " + condList
    connection = mySQLSettings.OpenConnection()
    df = pd.read_sql(sql, connection)
    return df


# Update Table:
def UpdateTable(_tblName, _headerCondition, _valueCondition, _headersUpdate, _valuesUpdate):
    sql = sqlSyntax.UpdateTableSQLCommands(_tblName, _headerCondition, _valueCondition, _headersUpdate, _valuesUpdate)
    RunSQL(sql)


def InsertRowToTable(_tblName, _header, _rowsTuple):
    tmp = ["%s" for x in range(len(_header))]
    strValue = ", ".join(tmp)
    sql = "INSERT INTO " + _tblName + " (" + ",".join(_header) \
          + ") VALUES" + "(" + strValue + ")"
    connection = mySQLSettings.OpenConnection()
    cursor = connection.cursor()
    cursor.executemany(sql, _rowsTuple)
    connection.commit()
    mySQLSettings.CloseConnection(connection)


def DeleteDatainTable(_tblName):
    sql = "DELETE FROM " + _tblName
    RunSQL(sql)


def RunSQL(_sql):
    connection = mySQLSettings.OpenConnection()
    cursor = connection.cursor()
    cursor.execute(_sql)
    connection.commit()
    mySQLSettings.CloseConnection(connection)


def InsertModelToDatabase(_tblName, _tblHeader, _modelId, _modelName, _stepIn, _stepOut, _predictType,
                          _feature, _name_to_int_set, _int_to_name_set, _currentVal_acc):
    _valueCondition = [_modelId, _modelName, _stepIn, _stepOut, _predictType, _feature, _name_to_int_set,
                       _int_to_name_set, _currentVal_acc]
    _valueCondition = ["'" + str(x) + "'" for x in _valueCondition]

    sql = "INSERT INTO " + _tblName + "(" + ", ".join(_tblHeader) + ")" \
          + " VALUES (" + ", ".join(_valueCondition) + ")"
    print(sql)
    SaveSQLInsertTraindModel(sql)
    # RunSQL(sql)
