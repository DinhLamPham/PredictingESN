# **Introduction**
# Process-Aware Enterprise Social Network Prediction and Experiment Using LSTM Neural Network Models
This repository is apart of the paper entitled "Process-Aware Enterprise Social Network Prediction and Experiment Using LSTM Neural Network Models".

DOI: 10.1109/ACCESS.2021.3071789

Summary:
...In this study, we apply the long short-term memory (LSTM) to predict an enterprise social network that is formed through information regarding a system’s operation. More precisely, we apply the multivariate multi-step LSTM model to predict not only the next activity and next performer, but also all the variants of a process-aware enterprise social network based on the next performer predictions using a probability threshold. Furthermore, we conduct an experimental evaluation on the real-life event logs and compare our results with baseline research. The results indicate that our approach creates a useful model to predict an enterprise social network and provides metrics to improve the operation of an information system based on the predicted information.


![The proposed LSTM architecture for predicting next activity and next performer](./propose_lstm_architecture.png)


Repository structure:
- Trained model folder: This folder contains the trained model for the data sets used in the paper: Help desk, BPI 2012, BPI 2015 - municipality 1, BPI 2015 - municipality 2, and BPI 2017
- Main/Train.py: Training model function.
- Main/PredictNext.py: Predict next event information (activities and performers)
- Main/PredictESN.py: Predict process-aware enterprise social network from the trained models.
- Main/EvaluateAccuracy.py: Evaluate the trained model (using the last 30% of the data sets for validation)



Note: If you want to reuse the repository for your study, remember to convert your log to the format described in 'Main/0 Helpdesk.txt'
