def UpdateTableSQLCommands(_tblName, _headerCondition, _valueCondition, _headerUpdate, _valueUpdate):
    conditionPara = _headerCondition + " ='" + _valueCondition + "'"
    valueList = []
    for x in zip(_headerUpdate, _valueUpdate):
        para = x[0] + " = '" + x[1] + "'"
        valueList.append(para)

    valuePara = (", ".join(valueList))
    result = "UPDATE " + _tblName + " SET " + valuePara \
             + " WHERE " + conditionPara

    return result


def InsertTableSQLCommands(_tblName, _headerCondition, _valueCondition):
    _valueCondition = ["'" + x + "'" for x in _valueCondition]

    # INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
    # VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
    result = "INSERT INTO " + _tblName + "(" + ", ".join(_headerCondition) + ")" \
             + "VALUES (" + ", ".join(_valueCondition) + ")"

    return result

