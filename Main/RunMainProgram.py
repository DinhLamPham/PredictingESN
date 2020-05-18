from MySQLHelper import Query, Connector
from CommonHelper.GVar import *

# Connector.OpenConnection()
# tblName = 'Performers'
# df = Query.ViewTable(tblName)
# print(df)
# ax = plt.gca()
# df.plot(kind='line', x='Name', y='InTotalTrace', ax=ax)
# df.plot(kind='line', x='Name', y='Occurence', color='red', ax=ax)
# plt.show()


myRows = [("summaryAct", "Image1", False),
          ("summaryAct", "Image1", False),
          ("summaryAct", "Image1", True)]
# Query.InsertRowToTable(tblFunctionResult, tblFunctionResultHeader, myRows)
Query.UpdateResultOfFunction(tblFunctionList, tblFunctionResultHeader, 'summaryAct', myRows)

Connector.CloseConnection()
