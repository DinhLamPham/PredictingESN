import os
from time import time
from pathlib import Path
from CommonHelper import GVar
from CommonHelper.Common import SaveDictToFile, LoadFileToDict, GetTrainedModelFolder
from CommonHelper.GVar import model_name, name_to_int_FileName, int_to_name_FileName, CombineTrace
from LogHelper.ReadFile import ReadSavedLog
from LogHelper.SaveTrainHistory import SaveAccuracy_Loss
from LogHelper.Trace import IntListToTraceSequence
from MachineLearningHelper.trainningHelper import prepare_os_environment, prepare_model, trainning, \
    one_hot_decode, lstm_get_data_from_trace
import gc
# from tensorflow.keras import backend


def cleanup_memory():
    # backend.clear_session()
    gc.collect()


prepare_os_environment()

start_time = time()

file = GVar.currentTrainingFile
logFolder = file.replace(".txt", "")

GVar.maxRepeatStep = 500

inputTrainingPara0 = [1, "Performer"]  # ok
inputTrainingPara1 = [1, "Activity"]  # ok
inputTrainingPara2 = [2, "Activity"]  # ok
inputTrainingPara3 = [2, "Performer"]  # ok
# inputTrainingPara4 = [2, "Activity_Performer"]  # ok

inputTrainingPara5 = [1.5, "1F_Activity_Performer"]  # ok

setOfPara = [inputTrainingPara0, inputTrainingPara1, inputTrainingPara2, inputTrainingPara3]
for para in setOfPara:
    inputTrainingPara = para
    GVar.Init_New_Log(inputTrainingPara)
    ReadSavedLog(file)

    logSize = len(GVar.traceWithEventList)
    split_point = int(logSize * 0.7)
    # split_point = 5
    train_log, test_log, train_combineLog, test_combineLog = None, None, None, None
    inputTrain, inputTest = None, None
    # Select dictionary
    if GVar.feature == 1:
        if GVar.predicttype == "Activity":
            current_name_to_int_set = GVar.act_to_int
            current_int_to_name_set = GVar.int_to_act
            train_log = GVar.traceWithActList[:split_point]
            test_log = GVar.traceWithActList[split_point:]

        if GVar.predicttype == "Performer":
            current_name_to_int_set = GVar.per_to_int
            current_int_to_name_set = GVar.int_to_per
            train_log = GVar.traceWithPerList[:split_point]
            test_log = GVar.traceWithPerList[split_point:]

        inputTrain, inputTest = train_log, test_log

    if GVar.feature == 2 or GVar.feature == 1.5:
        current_name_to_int_set = GVar.combine_to_int
        current_int_to_name_set = GVar.int_to_combine

        train_combineLog = CombineTrace(GVar.traceWithActList[:split_point], GVar.traceWithPerList[:split_point])
        test_combineLog = CombineTrace(GVar.traceWithActList[split_point:], GVar.traceWithPerList[split_point:])
        inputTrain, inputTest = train_combineLog, test_combineLog

    SaveDictToFile(current_name_to_int_set,
                   str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFolder) + GVar.name_to_int_FileName)
    SaveDictToFile(current_int_to_name_set,
                   str(Path(os.getcwd()).parent) + GetTrainedModelFolder(logFolder) + GVar.int_to_name_FileName)

    for stepIn in [1, 2, 3, 4, 5, 6]:
        GVar.n_in = stepIn
        for stepOut in [1, 2]:
            if stepIn < stepOut:
                continue
            GVar.n_out = stepOut
            GVar.batch_size = 1
            GVar.encoded_length = len(current_name_to_int_set)
            print("current gc: ", gc.get_count())
            gc.collect()
            print("after collecting gc: ", gc.get_count())
            model = prepare_model(current_name_to_int_set, GVar.predicttype)
            print(model.summary())

            accList, lossList = trainning(model, inputTrain, GVar.feature, current_name_to_int_set)
            SaveAccuracy_Loss(accList, lossList, model_name, GVar.feature, GVar.predicttype, GVar.n_in, GVar.n_out)

            cleanup_memory()
            del model
            gc.collect()
            end_time = time()
            time_taken = end_time - start_time  # time_taken is in seconds
            hours, rest = divmod(time_taken, 3600)
            minutes, seconds = divmod(rest, 60)

            print(stepIn, stepOut, "Total time: ", hours, minutes, int(seconds))

print('finished')
# load the saved model
# saved_model = load_model('best_model.h5')
# # evaluate the model
# _, train_acc = saved_model.evaluate(trainX, trainy, verbose=0)
# _, test_acc = saved_model.evaluate(testX, testy, verbose=0)
# print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

# # # # # # # # # # # # # # # # # # # # # # TEST # # # # # # # # # # # # # # # # # # # # #
# lenTest = 0
# if GVar.feature == 1:
#     lenTest = len(test_log)
# if GVar.feature == 2:
#     lenTest = len(test_combineLog.getAllTraceWithAct())
#
# for i in range(lenTest):
#     if GVar.feature == 1:
#         trace = train_log[i]
#     if GVar.feature == 2:
#         trace = test_combineLog.get_Trace_I_With_Combine(i)

#     X, y = lstm_get_data_from_trace(trace, GVar.predicttype, GVar.feature, current_name_to_int_set, GVar.n_in,
#                                     GVar.n_out)
#     yhat = model.predict(X, batch_size=GVar.batch_size, verbose=0)
# #
#     #     # decode all pairs
#     percent = [1 if one_hot_decode(y[i]) == one_hot_decode(yhat[i]) else 0 for i in range(len(X))]
#     print("Ti le du doan dung: ", sum(percent) / len(X))
#     for i in range(len(X)):
#         print("----------------------------------------------------------------")
#         print('Input:    ', IntListToTraceSequence(one_hot_decode(X[i]), current_int_to_name_set))
#         print('Expected: ', IntListToTraceSequence(one_hot_decode(y[i]), current_int_to_name_set))
#         print('Predicted:', IntListToTraceSequence(one_hot_decode(yhat[i]), current_int_to_name_set))

    # for x1, y1 in zip(X, y):
    #     current_in, current_out = np.reshape(x1, (-1, x1.shape[0], x1.shape[1])), np.reshape(y1, (
    #     -1, y1.shape[0], y1.shape[1]))
    #     y1hat = model.predict(current_in, batch_size=GVar.batch_size, verbose=0)
    #     print('Input: ', IntListToTraceSequence(one_hot_decode(current_in[0]), current_int_to_name_set))
    #     print('Expected:    ', IntListToTraceSequence(one_hot_decode(current_out), current_int_to_name_set))
    #     print('Output:    ', IntListToTraceSequence(one_hot_decode(y1hat), current_int_to_name_set))
