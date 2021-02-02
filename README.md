# PredictingESN
1. # **Introduction**

 _Predicting_ `enterprise` ~~social network from ev~~ent logs with LSTM network
           ` model = prepare_model(current_name_to_int_set, GVar.predicttype)
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

            print(stepIn, stepOut, "Total time: ", hours, minutes, int(seconds))`
            
  