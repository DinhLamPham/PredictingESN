import os
from pathlib import Path
import pandas as pd

from CommonHelper import GVar
from CommonHelper.Common import GetTrainedModelFolder


def SaveAccuracy_Loss(_accList, _lossList, _modelName, _feature, _predict, _n_in, _n_out):
    columns = ['Accuracy', 'Loss']
    df = pd.DataFrame(list(zip(_accList, _lossList)), columns=columns)
    fileName = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(GVar.model_name) \
               + _modelName + "_" + str(_feature) + "feature_" + _predict + str(_n_in) + "_" + str(_n_out) + ".xlsx"
    df.to_excel(fileName, index=False)


def SaveSQLInsertTraindModel(_sqlcmd):
    sqlFile = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(GVar.model_name) + "sqlcmd.txt"
    f = open(sqlFile, 'a')
    f.write(_sqlcmd + ";\n")
    f.close()
