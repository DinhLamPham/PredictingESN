import pandas as pd
from pandas import DataFrame, concat
actList = ['ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9']
perList = ['per1', 'per2', 'per3', 'per4', 'per5', 'per6', 'per7', 'per8', 'per9']

n_in = 3
# [actList.append("END") for _ in range(n_in)]
dfAct = DataFrame(actList)

dfX = DataFrame()
for i in range(0, n_in):
    currentVar = dfAct.shift(-i)
    dfX = concat([dfX, currentVar], axis=1)
dfX.dropna(inplace=True)

[perList.pop(0) for _ in range(n_in-1)]
dfy = DataFrame(perList)


