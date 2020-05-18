import os
from pathlib import Path
import pandas as pd

from CommonHelper.Common import GetPredictESNFolder


def SavePredictESNFile(_fileName, _keyWordSeparate, _keySeparateInside, _listResult):
    fileName = str(Path(os.getcwd()).parent.parent) + GetPredictESNFolder() + _fileName
    f = open(fileName, 'w')
    f.write(_keyWordSeparate + "\n")
    f.write(_keySeparateInside + "\n")
    for trace in _listResult:
        currentLine = _keyWordSeparate.join(trace)
        f.write(currentLine + "\n")
    f.close()

