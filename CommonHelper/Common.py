import pickle
import sys
import platform
import os

from CommonHelper import GVar

def CalculateAvgIn2DList(_2DList):
    mySum = 0
    countElemtn = 0
    for mylist in _2DList:
        mySum += sum(mylist)
        countElemtn += len(mylist)
    return mySum / countElemtn

def CalculateAvgIn1DList(_1DList):
    return sum(_1DList) / len(_1DList)

def get_platform():
    # Linux: Linux
    # Mac: Darwin
    # Windows: Windows
    return platform.system()


def GetTrainedModelFolder(_logName):
    currentOs = platform.system()
    if currentOs == 'Windows':
        return '\\' + GVar.trainedFolder + '\\' + _logName + '\\'
    else:
        # currentOs == 'Darwin' or currentOs == 'Linux':
        return '/' + GVar.trainedFolder + '/' + _logName + '/'


def GetGetTracesStatisticsFolder():
    currentOs = platform.system()
    if currentOs == 'Windows':
        return '\\' + GVar.GetTracesStatisticsFolder + '\\'
    else:
        # currentOs == 'Darwin' or currentOs == 'Linux':
        return '/' + GVar.GetTracesStatisticsFolder + '/'


def GetPredictESNFolder():
    currentOs = platform.system()
    if currentOs == 'Windows':
        return '\\' + GVar.predictESNFolder + '\\'
    else:
        # currentOs == 'Darwin' or currentOs == 'Linux':
        return '/' + GVar.predictESNFolder + '/'


def GetFileName(_inputName):
    output = _inputName.split('/')[-1].replace('.py', '')
    return output


def SaveDictToFile(_dict, _fileName):
    pickle_out = open(_fileName, "wb")
    pickle.dump(_dict, pickle_out)
    pickle_out.close()


def LoadFileToDict(_fileName):
    pickle_in = open(_fileName, "rb")
    myDict = pickle.load(pickle_in)
    return myDict


def iso_8601_format(_inputTime):
    import dateutil.parser
    myTime = dateutil.parser.parse(_inputTime)
    return myTime


# Iinput: 03:20:00 -> 3.3 hours; 3.3/24 day
def MyTime_In_String_To_Number(_inputTime, _convertType='H'):
    if _inputTime.find(':') < 0:
        return 0
    if _convertType == 'H':
        return int(_inputTime.split(':')[0]) + int(_inputTime.split(':')[1])/60
    else: # _convertType == 'D'
        return (int(_inputTime.split(':')[0]) + int(_inputTime.split(':')[1]) / 60) / 24


