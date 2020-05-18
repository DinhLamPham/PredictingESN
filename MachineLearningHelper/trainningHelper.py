import os
from pathlib import Path
from keras.models import load_model
import numpy as np

from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import Sequential
import platform

from numpy import argmax
from numpy import array
from pandas import DataFrame
from pandas import concat

from CommonHelper import GVar
from CommonHelper.Common import GetTrainedModelFolder, CalculateAvgIn2DList, CalculateAvgIn1DList
from LogHelper.Trace import TraceSequenceToIntList, TraceSequenceToIntList_WithoutAppend
from MySQLHelper.Query import InsertModelToDatabase
from matplotlib import pyplot as plt


def to_supervised_Act_Per(_actList, _perList, n_in):
    dfAct = DataFrame(_actList)

    dfX = DataFrame()
    for i in range(0, n_in):
        currentVar = dfAct.shift(-i)
        dfX = concat([dfX, currentVar], axis=1)
    dfX.dropna(inplace=True)

    for _ in range(n_in-1):
        _perList = np.delete(_perList, 0, 0)

    dfy = DataFrame(_perList)

    valuesX, valuesy = dfX.values, dfy.values

    X = valuesX.reshape(len(valuesX), n_in, -1)
    y = valuesy.reshape(len(valuesy), 1, -1)

    return X, y

def to_supervised(sequence, n_in, n_out):
    # create lag copies of the sequence
    df = DataFrame(sequence)

    dfX = concat([df.shift(i) for i in range(n_in, 0, -1)], axis=1)
    dfy = concat([df.shift(-(n_in + i)) for i in range(0, n_out)], axis=1)
    # drop rows with missing values
    dfX.dropna(inplace=True)
    dfy.dropna(inplace=True)
    # specify columns for input and output pairs
    valuesX, valuesy = dfX.values, dfy.values

    X = valuesX.reshape(len(valuesX), n_in, -1)
    y = valuesy.reshape(len(valuesy), n_out, -1)
    # (len(X) - len(y) => redundance input. No output
    X = X[0:len(y)]
    return X, y


# one hot encode sequence
def one_hot_encode(sequence, n_unique):
    encoding = list()
    for value in sequence:
        vector = [0 for _ in range(n_unique)]
        vector[value] = 1
        encoding.append(vector)
    return array(encoding)


def one_hot_decode(encoded_seq):
    result = [argmax(vector) for vector in encoded_seq]
    return result


def multi_decode_with_top_rank(_inputSeq, _topRank):
    _inputSeq = _inputSeq.reshape(-1)
    indices = list(range(len(_inputSeq)))
    indices.sort(key=lambda y: _inputSeq[y], reverse=True)
    result = indices[:int(_topRank)]
    return result


def multi_decode_with_probability(encoded_seq, _probability):
    result = []
    listProb = encoded_seq.reshape(-1)
    for idx, val in enumerate(listProb):
        if val >= _probability:
            result.append(idx)

    return result


def encode_trace_sequence(_inputTrace,  name_to_int_set={}):
    sequence = TraceSequenceToIntList(_inputTrace, name_to_int_set)
    encoded = one_hot_encode(sequence, len(name_to_int_set))
    encoded = encoded.reshape(1, len(_inputTrace), -1)
    return encoded

# Convert trace to X, y in vector. X->y
def lstm_get_data_from_trace(trace, _predictType="Activity", _feature=1, name_to_int_set={}, n_in=1, n_out=1):
    if _feature == 1:
        # generate random sequence
        sequence = TraceSequenceToIntList(trace, name_to_int_set)
        # one hot encode
        encoded = one_hot_encode(sequence, len(name_to_int_set))
        # convert to X,y pairs
        X, y = to_supervised(encoded, n_in, n_out)
        return X, y
    if _feature == 1.5:
        sequenceAct = trace.getAllTraceWithAct()
        sequenceAct = TraceSequenceToIntList_WithoutAppend(sequenceAct, name_to_int_set)
        encodedAct = one_hot_encode(sequenceAct, len(name_to_int_set))

        sequencePer = trace.getAllTraceWithPer()
        sequencePer = TraceSequenceToIntList_WithoutAppend(sequencePer, name_to_int_set)
        encodedPer = one_hot_encode(sequencePer, len(name_to_int_set))

        X, y = to_supervised_Act_Per(encodedAct, encodedPer, n_in)
        return X, y

    if _feature == 2:
        # generate random sequence
        sequenceAct = trace.getAllTraceWithAct()
        sequenceAct = TraceSequenceToIntList(sequenceAct, name_to_int_set)
        encodedAct = one_hot_encode(sequenceAct, len(name_to_int_set))
        Xact, yact = to_supervised(encodedAct, n_in, n_out)

        sequencePer = trace.getAllTraceWithPer()
        sequencePer = TraceSequenceToIntList(sequencePer, name_to_int_set)
        encodedPer = one_hot_encode(sequencePer, len(name_to_int_set))
        Xper, yper = to_supervised(encodedPer, n_in, n_out)

        Xreturn = ConcatenateTwoFeatures(Xact, Xper, n_in, _feature, name_to_int_set)

        if _predictType == "Activity":
            yreturn = yact
        if _predictType == "Performer":
            yreturn = yper
        if _predictType == "Activity_Performer":
            yreturn = ConcatenateTwoFeatures(yact, yper, n_out, _feature, name_to_int_set)

        return Xreturn, yreturn


def ConcatenateTwoFeatures(act, per, step, _feature, name_to_int_set):
    act = np.reshape(act, (-1, step * len(name_to_int_set)))
    per = np.reshape(per, (-1, step * len(name_to_int_set)))
    combine = np.concatenate((act, per), axis=1)
    combine = np.reshape(combine, (-1, step * _feature, len(name_to_int_set)))
    return combine


# Convert n_in step to Vector
def lstm_get_data_from_n_in(_inputList, name_to_int_set, n_in):
    sequence = TraceSequenceToIntList(_inputList, name_to_int_set)
    encoded = one_hot_encode(sequence, len(name_to_int_set))

def prepare_model(_name_to_int_set, _predictType):
    model = None
    model = Sequential()
    _feature = int(GVar.feature)
    model.add(
        LSTM(150, batch_input_shape=(GVar.batch_size, GVar.n_in * _feature, GVar.encoded_length),
             stateful=True))
    if _predictType == "Activity_Performer": # 2 feature output: actvity, performer => Ouput cell: N_step_out * ouputfeature
        model.add(RepeatVector(GVar.n_out * 2))
    else: # Only one output feature: activity/performer => Ouputcell: N_step_out * 1
        model.add(RepeatVector(GVar.n_out * 1))
    model.add(LSTM(150, return_sequences=True, stateful=True))
    model.add(TimeDistributed(Dense(len(_name_to_int_set), activation='softmax')))
    # model.add(TimeDistributed(Dense(GlobalVariables.n_out, activation='softmax')))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def trainning(model, train_log, _feature=1, _current_name_to_int_set={}):

    es = EarlyStopping(monitor='accuracy', mode='max', patience=50)
    mc = ModelCheckpoint(GVar.model_name, monitor='accuracy',
                         mode='max', verbose=1, save_best_only=True)
    countEpoch, maxVal_acc, totalTrace, accuracy_list, loss_list, trace = 0, 0, 0, [], [], []

    if _feature == 1:
        totalTrace = len(train_log)
    if _feature == 2 or _feature == 1.5:
        totalTrace = len(train_log.getAllTraceWithAct())

    for i in range(totalTrace):
        traceLength = 0
        if _feature == 1:
            trace = train_log[i]
            traceLength = len(trace)
        if _feature == 2 or _feature == 1.5:
            trace = train_log.get_Trace_I_With_Combine(i)
            traceLength = train_log.get_Trace_Length(i)

        if traceLength < (GVar.n_in + GVar.n_out):
            print("len of trace %d < in+out" % i)
            continue

        X, y = lstm_get_data_from_trace(trace, GVar.predicttype, _feature, _current_name_to_int_set, GVar.n_in, GVar.n_out)

        history = model.fit(X, y, epochs=1, batch_size=GVar.batch_size, verbose=2,
                            shuffle=True)
        currentMax_acc = max(history.history['accuracy'])
        accuracy_list.append(history.history['accuracy'][0])
        loss_list.append(history.history['loss'][0])

        if currentMax_acc > maxVal_acc:
            maxVal_acc = currentMax_acc
            countEpoch = 0
        else:
            countEpoch += 1
        if countEpoch > GVar.maxRepeatStep:
            print("Training should stop here, save model, then exist")
            # Save modelFilename, name_to_int_set, int_to_name_set
            # ------------_Temporary pause---------------------
            SaveModel(model, accuracy_list)

            # ------------_Temporary pause---------------------
            return accuracy_list, loss_list

        print(
            "------------------------------------------------trace (%s / %s) ------ Count patient trace: %s"
            " --- currentMax: %s" % (i, totalTrace, countEpoch, maxVal_acc))
        model.reset_states()

    SaveModel(model, accuracy_list)
    model = None
    return accuracy_list, loss_list


def SaveModel(_model, _accuracy_list):
    modelId = GVar.model_name + str(GVar.feature) + "feature_" + GVar.predicttype + str(GVar.n_in) + "_" \
              + str(GVar.n_out) + ".h5"
    InsertModelToDatabase(GVar.tblModel, GVar.tblModelHeader, modelId,
                          GVar.model_name, GVar.n_in, GVar.n_out,
                          GVar.predicttype, GVar.feature,
                          GVar.name_to_int_FileName, GVar.int_to_name_FileName,
                          CalculateAvgIn1DList(_accuracy_list))
    fileToSave = str(Path(os.getcwd()).parent) + GetTrainedModelFolder(GVar.model_name) + modelId
    _model.save(fileToSave)

def prepare_os_environment():
    if platform.system() == 'Darwin':  # Mac OS
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    return 1
    # os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # config = tf.ConfigProto(intra_op_parallelism_threads=0,
    #                         inter_op_parallelism_threads=0,
    #                         allow_soft_placement=True)
    # session = tf.Session(config=config)


def CalculateBatchSize(_inputSize):
    for i in range(10, 2, -1):
        if _inputSize % i == 0:
            return i
    return _inputSize


def Predict(_modelFileName, _stepIn, _stepOut, _predictType, _feature, _inputList):
    saved_model = load_model('best_model.h5')
    # X, y = lstm_get_data(trace, current_name_to_int_set, GlobalVariables.n_in, GlobalVariables.n_out)
    # yhat = model.predict(X, batch_size=GlobalVariables.batch_size, verbose=0)
