# **Introduction**
# Prediction of Process-Aware Enterprise Social Networks 
This repository is apart of the paper entitled "Prediction of Process-Aware Enterprise Social Networks and its Experiments Using Long Short-Term Memory Neural Network Models".

Summary:
...In this study, we apply the long short-term memory (LSTM) to predict an enterprise social network that is formed through information regarding a system’s operation. More precisely, we apply the multivariate multi-step LSTM model to predict not only the next activity and next performer, but also all the variants of a process-aware enterprise social network based on the next performer predictions using a probability threshold. Furthermore, we conduct an experimental evaluation on the real-life event logs and compare our results with baseline research. The results indicate that our approach creates a useful model to predict an enterprise social network and provides metrics to improve the operation of an information system based on the predicted information.

Repository structure:
- Trained model folder: This folder contains the trained model for the data sets used in the paper: Help desk, BPI 2012, BPI 2015 - municipality 1, BPI 2015 - municipality 2, and BPI 2017
- Main/Train.py: Training model function.
- Main/PredictNext.py: Predict next event information (activities and performers)
- Main/PredictESN.py: Predict process-aware enterprise social network from the trained models.
- Main/EvaluateAccuracy.py: Evaluate the trained model (using the last 30% of the data sets for validation)
