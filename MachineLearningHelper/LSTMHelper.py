# import os
# from random import randint
#
# from matplotlib import pyplot
# from numpy import array
# from numpy import argmax
# from pandas import DataFrame
# from pandas import concat
# from keras.models import Sequential
# from keras.layers import LSTM
# from keras.layers import Dense
# from keras.layers import TimeDistributed
# from keras.layers import RepeatVector
# import tensorflow as tf
#
# from time import time
# start_time = time()
#
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
# config = tf.ConfigProto(intra_op_parallelism_threads=0,
#                         inter_op_parallelism_threads=0,
#                         allow_soft_placement=True)
# session = tf.Session(config=config)
#
# numberRange = 100
# listLen = 25
#
#
# # generate a sequence of random numbers in [0, 99]
# def generate_sequence(length=listLen):
#     # return [randint(0, numberRange - 1) for _ in range(length)]
#     first5 = [randint(0, 5) for _ in range(5)]
#     result = first5
#     for i in range(5, length):
#         currence = sum(result[i-3: i-1]) - result[i-1]
#         if currence < 0 or currence >= 100:
#             currence = result[i-1]
#         result.append(currence)
#     return result
#
#
# # one hot encode sequence
# def one_hot_encode(sequence, n_unique=numberRange):
#     encoding = list()
#     for value in sequence:
#         vector = [0 for _ in range(n_unique)]
#         vector[value] = 1
#         encoding.append(vector)
#     return array(encoding)
#
#
# # decode a one hot encoded string
# def one_hot_decode(encoded_seq):
#     return [argmax(vector) for vector in encoded_seq]
#
#
# # convert encoded sequence to supervised learning
# def to_supervised(sequence, n_in, n_out):
#     # create lag copies of the sequence
#     df = DataFrame(sequence)
#
#     dfX = concat([df.shift(i) for i in range(n_in, 0, -1)], axis=1)
#     dfy = concat([df.shift(-(n_in + i)) for i in range(0, n_out)], axis=1)
#     # drop rows with missing values
#     dfX.dropna(inplace=True)
#     dfy.dropna(inplace=True)
#     # specify columns for input and output pairs
#     valuesX, valuesy = dfX.values, dfy.values
#
#     X = valuesX.reshape(len(valuesX), n_in, -1)
#     y = valuesy.reshape(len(valuesy), n_out, -1)
#     # (len(X) - len(y) => redundance input. No output
#     X = X[0:len(y)]
#     return X, y
#
#
# # convert encoded sequence to supervised learning
# def to_supervised_old(sequence, n_in, n_out):
#     # create lag copies of the sequence
#     df = DataFrame(sequence)
#     df = concat([df.shift(n_in - i - 1) for i in range(n_in)], axis=1)
#     # drop rows with missing values
#     df.dropna(inplace=True)
#     # specify columns for input and output pairs
#     values = df.values
#     width = sequence.shape[1]
#     X = values.reshape(len(values), n_in, width)
#     y = values[:, 0:(n_out * width)].reshape(len(values), n_out, width)
#     return X, y
#
#
# # prepare data for the LSTM
# def get_data(n_in, n_out):
#     # generate random sequence
#     sequence = generate_sequence()
#     # one hot encode
#     encoded = one_hot_encode(sequence)
#     # convert to X,y pairs
#     X, y = to_supervised(encoded, n_in, n_out)
#     return X, y
#
#
#
# # define LSTM
# n_in = 6
# n_out = 2
# encoded_length = 100
# batch_size = 6
# model = Sequential()
# model.add(LSTM(150, batch_input_shape=(batch_size, n_in, encoded_length), stateful=True))
# model.add(RepeatVector(n_out))
# model.add(LSTM(150, return_sequences=True, stateful=True))
# model.add(TimeDistributed(Dense(encoded_length, activation='softmax')))
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# print(model.summary())
# # train LSTM
# for epoch in range(500):
#     # generate new random sequence
#     X, y = get_data(n_in, n_out)
#     print("------------------------------Sequence: ", epoch, "-------------------------")
#     # fit model for one epoch on this sequence
#     model.fit(X, y, epochs=15, batch_size=batch_size, verbose=2, shuffle=False)
#     model.reset_states()
#
# end_time = time()
# time_taken = end_time - start_time  # time_taken is in seconds
# hours, rest = divmod(time_taken, 3600)
# minutes, seconds = divmod(rest, 60)
# print("Total time: ", hours, minutes, int(seconds))
# # evaluate LSTM
# while True:
#     X, y = get_data(n_in, n_out)
#     yhat = model.predict(X, batch_size=batch_size, verbose=0)
#     # decode all pairs
#     percent = [1 if one_hot_decode(y[i]) == one_hot_decode(yhat[i]) else 0 for i in range(len(X))]
#     print("Ti le du doan dung: ", sum(percent)/len(X))
#     for i in range(len(X)):
#         print('Input:    ', one_hot_decode(X[i]))
#         print('Expected: ', one_hot_decode(y[i]))
#         print('Predicted:', one_hot_decode(yhat[i]))
