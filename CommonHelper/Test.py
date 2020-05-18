from CommonHelper.GVar import *


def Combine(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate):

    conditionPara = _headerCondition + " ='" + _valueCondition + "'"
    valueList = []
    for x in zip(_headerUpdate, _valueUpdate):
        para = x[0] + " = '" + x[1] + "'"
        valueList.append(para)

    valuePara = (", ".join(valueList))
    result = "UPDATE " + _tblName + " SET " + valuePara \
             + " WHERE " + conditionPara

    return result


myList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for step in range(5):
    print(myList[-step:])



_tblName = tblFunctionList
_headerCondition = 'id'
_valueCondition = 'myfunc'

_headerUpdate = ['output', 'display']
_valueUpdate = ['abc/def', 'False']
Combine(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate)
