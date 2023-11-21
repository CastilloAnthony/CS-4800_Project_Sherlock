# Created by Anthony Castillo

import time
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
class PredictionModel():
    """This class is designed to create a model, train the model on data, make future predictions on data, generate (temporary) graphs on and return those predictions. NOTE: This is still a WIP and is subject to change. In fact, a lot of this will be removed and possibly refactored.
    Created by Anthony Castillo.
    """
    def __init__(self):
        """Initializes most variables to False
        """
        self.__train_data = False
        self.__val_data = False
        self.__test_data = False
        self.__model = False
        self.__size = 0
        self.__train_ds = False
        self.__val_ds = False
        self.__test_ds = False
        self.__modelFilename = 'Unknown.keras'
        self.__avgDist = 1
        self.__sampleRate = '30T'
        self.__name = False
        self.__originalDataCleaned = False
        self.__multiprocess = True

    def __del__(self):
        """Deletes variables
        """
        del self.__train_data, self.__val_data, self.__test_data, self.__model, self.__modelFilename, self.__size, self.__train_ds, self.__val_ds, self.__test_ds, self.__avgDist, self.__sampleRate, self.__name, self.__originalDataCleaned, self.__multiprocess

    def createModel(self):
        """Creates, builds, and assigns a new model for this class to use.
        """
        self.__model = tf.keras.Sequential([
            #tf.keras.layers.Lambda(lambda x: x[:, -2:, :]),
            #tf.keras.Input(shape=(int(self.__size*0.7))), #, int(self.__size*0.7))),
            #tf.keras.layers.Reshape((int(self.__size*0.7*0.5), 2), input_shape=(int(self.__size*0.7),)),# dtype=tf.float32), # int(int(self.__size*0.7)//(self.__size*0.7*0.5))
            #tf.keras.layers.Dense(256, activation='LeakyReLU'),# input_shape=(32,)),#(self.__size*0.7), 2)),
            #tf.keras.layers.Dropout(0.2),
            #tf.keras.layers.Reshape((16, 16)),#, input_shape=(128, 256,)),
            #tf.keras.layers.Conv1D(32, 3, activation='relu'),
            #tf.keras.layers.Dropout(0.1),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Reshape((1, 1,)),# input_shape=(32,)),
            tf.keras.layers.LSTM(1024, return_sequences=True), # Recurrent Neural 
            tf.keras.layers.LSTM(512, return_sequences=True),
            tf.keras.layers.LSTM(256, return_sequences=True),
            tf.keras.layers.LSTM(128, return_sequences=True),
            tf.keras.layers.LSTM(64, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(32, activation='tanh', return_sequences=True, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.LSTM(16, return_sequences=True),
            tf.keras.layers.LSTM(8, return_sequences=True),
            tf.keras.layers.LSTM(4, return_sequences=True),
            tf.keras.layers.LSTM(2, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(1, return_sequences=True),
            #tf.keras.layers.LSTM(512, return_sequences=True),
            #tf.keras.layers.RNN(tf.keras.layers.LSTMCell(256), return_state=True),
            #tf.keras.layers.Conv2D(256 activation='LeakyReLU')
            #tf.keras.layers.Dropout(0.2),
            #tf.keras.layers.Flatten(),
            #tf.keras.layers.Dense(128, activation='gelu'), #input_shape=(int(self.__size*0.7), 2)),
            #tf.keras.layers.Dense(128),
            #tf.keras.layers.Dropout(0.1),
            #tf.keras.layers.Dense(2, activation='softmax'),# input_shape=(int(self.__size*0.7), 2))
            #tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(1),
        ])
        #loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
        
        self.__model.compile(
            optimizer='sgd',#tf.keras.optimizers.Adam(learning_rate=0.001), 
            loss=tf.keras.losses.MeanSquaredError(),#tf.keras.losses.Huber(),#tf.keras.losses.LogCosh(),#'mse', 
            metrics=['mae', 'mse',]#['accuracy']
            )#'sparse_categorical_crossentropy')#'mse')#loss_fn,)
        #print(len(self.__model.weights))
        #print(self.__model.get_config())
        self.__model.build(input_shape=(32, 1,))
        #self.__model.summary()
        #print("Model Input Shape:", self.__model.input_shape)
        '''
        Image Model Example
        self.__model = tf.keras.Sequential([
        #tf.keras.layers.Resizing(img_height, img_width), # Done with data preprocessing
        #tf.keras.layers.Rescaling(1./255), # Done with data preprocessing
        tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu', input_shape=(180, 180, 3)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(180, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(classCount, activation='softmax')
        #tf.keras.layers.Dense(256, activation='LeakyReLU', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        #tf.keras.layers.Dropout(0.2),
        #tf.keras.layers.Dense(128, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2(0.01)),#'sigmoid', 'relu', 'softmax', 'LeakyReLU' 
        #tf.keras.layers.Dense(2, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        #tf.keras.layers.Flatten(),
        ])
        '''

    def saveModel(self):
        """Saves the model to a file using the name provided in self.__modelFilename
        """
        try:
            #self.__model.summary()
            self.__model.save(self.__modelFilename)
        except:
            print('Could not save prediction model.')

    def readModel(self):
        """Reads a model from file using the name provided in self.__modelFilename
        """
        try:
            self.__model = tf.keras.models.load_model(self.__modelFilename)
            #self.__model.summary()
        except:
            self.createModel()

    def setFilename(self, name:str):
        """Changes the file name that the model gets saved as. Additionally creates a new model and then saves it to the new file.

        Args:
            name (str): The name to change the model's file
        """
        self.__name = name
        self.__modelFilename = 'predictionModels/'+name+'.keras'
        #self.__modelFilename = 'predictionModels/'+name+'_'+self.__sampleRate+'.keras'
        #self.__modelFilename = 'predictionModels/'+'mainModel'+'.keras'
        #self.createModel()
        #self.saveModel()

    def getFilename(self):
        """Returns the name of the file that the model is saved in

        Returns:
            str: The name of the file the model is saved to
        """
        return self.__modelFilename

    def setData(self, data:np.array):
        """Clears out the old data and then sets the new data in the class.

        Args:
            data (list): A list of dictionaries to work with (i.e., [{data0}, {data1}, {data2}])
        """
        self.clearData()
        tempDataX = data[0] # Timestamp
        tempDataY = data[1]*100 # Latency
        #print(tempDataY[0], tempDataY[-1])
        #tempMean = 
        #print(tempMean, tempMean**2)
        #print(len(tempDataX))
        #for i, v in enumerate(tempDataX):
        i=0
        while i < len(tempDataX):
            if np.isnan(tempDataX[i]) or np.isnan(tempDataY[i]):
                tempDataX = np.delete(tempDataX, i)
                tempDataY = np.delete(tempDataY, i)
            elif tempDataY[i] == 0:
                tempDataX = np.delete(tempDataX, i)
                tempDataY = np.delete(tempDataY, i)
            elif tempDataY[i] > np.nanmean(tempDataY)**2:
                tempDataX = np.delete(tempDataX, i)
                tempDataY = np.delete(tempDataY, i)
            i += 1
        #print(np.nanmean(tempDataY), np.nanmean(tempDataY)**2)

        self.__size = len(tempDataX)
        #print('Starting Size: ', self.__size, int(self.__size*0.7))
        while int(self.__size*0.7)%2 != 0:#self.isOdd(int(self.__size*0.7)): # 
            tempDataX = np.delete(tempDataX, 0, None)
            tempDataY = np.delete(tempDataY, 0, None)
            self.__size = len(tempDataX)
            #print(self.__size, int(self.__size*0.7))
        #print('Ending Size: ', self.__size, int(self.__size*0.7))
        #tempData = np.vstack((tempDataX, tempDataY))
        #print(tempDataY*100)
        #print(np.nanmean(tempDataY), np.nanstd(tempDataY))
        #print(tempDataY.mean(), tempDataY.std())
        #test = np.vstack((tempDataX, tempDataY,))
        #print(test)
        # \/ Modify this \/
        tempDF = pd.DataFrame({'timestamp':tempDataX, 'latency':tempDataY,}, index=pd.to_datetime(tempDataX, unit='s'))#.resample(self.__sampleRate).mean()
        self.__originalDataCleaned = tempDF
        # for i, v in enumerate(tempDF['timestamp']):
        #     if np.isnan(v):
        #         tempDF['timestamp'].drop(index=i, inplace=True)
        #     #tempDF['latency'][i].replace(tempDF['latency'].mean(), np.nan, inplace = True)
        tempDF = tempDF.dropna(subset=['latency'])
        #print(tempDF.head())
        self.__size = len(tempDF['latency'])
        #print(tempDF['timestamp'])
        #print(tempDF['latency'])
        #print(tempDF[0], tempDF[1])
        #print(tempDF.index)
        #print(tempDF[0])

        timestampData = tempDF['timestamp'].to_numpy()#tempDataX
        latencyData = tempDF['latency'].to_numpy()#tempDataY
        #plt.pyplot.plot(pd.to_datetime(tempDF['timestamp'], unit='s'), tempDF['latency'], 'o-')
        #plt.pyplot.show()
        '''
        # Timestamp
        train_dataX = timestampData[0:int(self.__size*0.7)]
        val_dataX = timestampData[int(self.__size*0.7):int(self.__size*0.9)]
        test_dataX = timestampData[int(self.__size*0.9):]

        # Latency
        train_dataY = latencyData[0:int(self.__size*0.7)]
        val_dataY = latencyData[int(self.__size*0.7):int(self.__size*0.9)]
        test_dataY = latencyData[int(self.__size*0.9):]

        train_mean = np.nanmean(train_dataY)
        train_std = np.nanstd(train_dataY)

        self.__train_data = np.vstack((train_dataX, train_dataY))
        self.__val_data = np.vstack((val_dataX, val_dataY))
        self.__test_data = np.vstack((test_dataX, test_dataY))
        '''
        self.__train_data = np.vstack((tempDF['timestamp'][0:int(self.__size*0.7)], tempDF['latency'][0:int(self.__size*0.7)]))
        self.__val_data = np.vstack((tempDF['timestamp'][int(self.__size*0.7):int(self.__size*0.9)], tempDF['latency'][int(self.__size*0.7):int(self.__size*0.9)]))
        self.__test_data = np.vstack((tempDF['timestamp'][int(self.__size*0.9):], tempDF['latency'][int(self.__size*0.9):]))
        
        #print(self.__train_data)
        # print('Training Data:\n', self.__train_data)
        # print('Validation Data:\n', self.__val_data)
        # print('Test Data:\n', self.__test_data)
        # print('Length: ', self.__size, '70%: ', int(self.__size*0.7), ' ', 'Mean: ', train_mean, ' ', 'STD: ', train_std)

        # Normalizing data
        #self.__train_data[1] = abs((self.__train_data[1] - train_mean) / train_std)
        #self.__val_data[1] = abs((self.__val_data[1] - train_mean) / train_std)
        #self.__test_data[1] = abs((self.__test_data[1] - train_mean) / train_std)

        #print(self.__train_data[0][0])
        #print(self.__train_data[0][1])
        #print(self.__train_data[0][-1])
        temptemptemp = np.empty(1)
        #print(self.__size, len(train_dataX)-1)
        #print('Length of Training Data:', len(self.__train_data[0]), int(self.__size*0.7), self.__train_data[0][0+1]-self.__train_data[0][0])
        #print(range(0, int(self.__size*0.7)-2))
        for i in range(0, int(self.__size*0.7)-2):
            #print('Calculating ', i, self.__train_data[0][i])
            temptemptemp = np.append(temptemptemp, self.__train_data[0][i+1]-self.__train_data[0][i])
        temptemptemp =temptemptemp[~np.isnan(temptemptemp)]
        #print('temptemptemp:', len(temptemptemp), np.average(temptemptemp), temptemptemp,)
        self.__avgDist = np.average(temptemptemp)
        #print(np.average(temptemptemp))
        # print('Training Data:\n', train_data)
        # print('Validation Data:\n', val_data)
        # print('Test Data:\n', test_data)
        #print(tf.shape(self.__train_data[0]))
        
        # self.__train_ds = tf.keras.utils.timeseries_dataset_from_array(
        #     data=self.__train_data[1],
        #     targets=self.__train_data[0],
        #     sequence_length=int(self.__train_data.size*0.7),
        #     sequence_stride=1,
        #     shuffle=False,
        #     batch_size=32
        # )
        # self.__val_ds = tf.keras.utils.timeseries_dataset_from_array(
        #     data=self.__val_data[1],
        #     targets=self.__val_data[0],
        #     sequence_length=int(self.__val_data.size*0.9-self.__val_ds*0.7),
        #     sequence_stride=1,
        #     shuffle=False,
        #     batch_size=32
        # )

        # self.__train_ds = tf.data.Dataset.from_tensor_slices((self.__train_data[1], self.__train_data[0]))
        # self.__val_ds = tf.data.Dataset.from_tensor_slices((self.__val_data[1], self.__val_data[0]))

        #self.__train_ds = tf.data.Dataset.from_tensor_slices((self.__train_data[1], self.__train_data[0]))
        #self.__val_ds = tf.data.Dataset.from_tensor_slices((self.__val_data[1], self.__val_data[0]))
        #self.__test_ds = tf.data.Dataset.from_tensor_slices((self.__test_data[1], self.__test_data[0]))
        
        #print('Shape of train_data:', tf.shape(self.__train_data))
        #print('Cardinality of Train_ds:', tf.data.experimental.cardinality(self.__train_ds))
        
        #print('Shape of train_ds:', tf.shape(self.__train_ds))
        #print(train_ds, val_ds)
        #train_latency = self.__data['latency'] - train_mean / train_std
        #val_latency = tf.keras.utils.timeseries_dataset_from_array()
        #print(len(self.__train_data), len(self.__train_data[0]), len(self.__train_data[1]))

    def clearData(self):
        """Empties the data that is currently stored by the model
        """
        self.__train_data = False
        self.__val_data = False
        self.__test_data = False
        self.__originalDataCleaned = False

    def clearModel(self):
        """Resets the model back to a skeleton model (i.e., no training.)
        """
        self.__model = False
        self.createModel()
    
    def predict(self, quantity:int=60*60*12):
        """DEPRECATED, Projects the future for the current data using the fitted model.

        Args:
            quantity (int, optional): The number of minutes to project over. Defaults to 60*3.

        Returns:
            list: A list of all the predictions
        """
        # https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing
        #print(self.__train_data[0], self.__train_data[0][0], self.__train_data[0][1])
        #print(self.__train_data[0][-1], self.__train_data[0][-1]+quantity, self.__avgDist, self.__train_data[0][-1]+quantity-self.__train_data[0][-1])
        temp = np.arange(self.__train_data[0][-1]+self.__avgDist, self.__train_data[0][-1]+quantity, self.__avgDist)
        #print(temp)
        temptemp = []
        predictions = []
        #print(len(temp), temp)
        for i, v in enumerate(temp):
            #print(i, v)
            predictions = np.append(predictions, self.__model.predict([v]).flatten())
            temptemp = np.append(temptemp, temp[i])
            #print(temptemp, predictions)
            #self.trainModel(data=np.vstack((temptemp, predictions)), patience=10)
        #predictions = self.__model.predict(temp).flatten()#tf.expand_dims(self.__data, axis=0))
        
        #print('Precitions Output: ',len(predictions), 'Shape:', print(predictions.shape), print(predictions))
        
        #outputDF = pd.DataFrame(predictions) # [{'data0'}, {'data1'}, {'data2'}, {'etc.'}, {'data#quantity-1#'}]
        #outputDF.add()
        #test = []
        #for i in predictions[0]:
            #test.append(i[0])
        #plt.pyplot.plot(data[0], data[1], 'o', label='Original Data')
        #print(predictions[0][1])

        #tempY = outputDF[0].to_numpy()
        tempY = predictions
        tempDF = pd.DataFrame({'timestamp':temp, 'latency':tempY,}, index=pd.to_datetime(temp, unit='s')).resample(self.__sampleRate).mean()
        tempDF = tempDF.dropna(subset=['timestamp'])
        tempDF = tempDF.dropna(subset=['latency'])
        #print(temp)
        #print(predictions)
        #print(tempY)
        #print(outputDF)
        ''''
        with open('temp.txt', 'w') as file:
            file.writelines('Training Data:\n')
            for i, v in enumerate(self.__train_data[0]):
                file.writelines(str(i)+'\t|\t'+str(v)+'\t|\t'+str(self.__train_data[1][i])+'\n')
        with open('temp.txt', 'a') as file:
            file.writelines('Predictions:\n')
            for i, v in enumerate(tempDF['timestamp']):
                file.writelines(str(i)+'\t|\t'+str(v)+'\t|\t'+str(tempDF['latency'][i])+'\n')
        '''
        #print(tempDF.head())
        self.graph(tempDF)
        return np.vstack((temp, tempY))

    def graph(self, tempDF, secondData=None, sampleRate='5T'):
        """Generates and saves a graph

        Args:
            tempDF (np.array): A two dimensional array containing timestamps on the first axis and latency values on the second axis.
            secondData (np.array, optional): Similar to above, but optional. Defaults to None.
            sampleRate (str, optional): The rate for which data is resampled to, this cleans up the graphs and makes them look less cluttered. Defaults to '5T'.
        """
        if secondData != None:
            tempXData = self.__originalDataCleaned.resample(sampleRate).mean()
        fig, axes = plt.subplots(1,1, figsize=(16*1.0,9*1.0)) # plt.subplots(nrows, ncolumns, *args) # axs will be either an individual plot or an array of axes
        try:
            ax = axes[0,0] # If axes is a 2D array of axes, then we'll use the first axis for this drawing.
        except:
            try:
                ax = axes[0] # If axes is a 1D array of axes, then we'll use the first axis for this drawing.
            except:
                ax = axes # If axes is just a single axis then we'll use it directly.
        fig.autofmt_xdate()
        ax.grid(which='both',axis='both')
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6, tz='US/Pacific'))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1, tz='US/Pacific'))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        ax.set_ylabel('Latency (ms)')
        ax.set_title('Average ('+self.__sampleRate+') Latency of '+self.__name)
        if secondData != None:
            plot1, = ax.plot(tempXData[0].astype('datetime64[s]'), tempXData[1], 'o-', alpha=1.0, label='Normalized Data')
        plot2, = ax.plot(pd.to_datetime(tempDF['timestamp'], unit='s'), tempDF['latency'], 'o-', alpha=0.5, label='Predictions')
        #ax.fmt_xdata = plt.dates.DateFormatter('%Y-%m-%d')
        #plt.pyplot.plot(temp.astype('datetime64[s]'), tempY, 'o', alpha=0.5, label='Predictions')
        if secondData !=None:
            plt.legend(handles=[plot1, plot2], loc='best')
        else:
            plt.legend(handles=[plot2], loc='best')
        plt.tight_layout()
        plt.savefig('gallery/'+self.__name+'_'+self.__sampleRate+'_'+str(time.time())+'.png')
        plt.clf()
        print(str(time.ctime())+' - A new graph for '+self.__name+' has been generated...')
        #plt.show()

    def trainModel(self, epochs:int=10*10**2, data=None, patience:int=25):
        """DEPRECATED, Trians the model on the data given using the 

        Args:
            iterations (int, optional): The number of time the model will be fitted to the data. Defaults to 3.
        """
        #https://www.tensorflow.org/tutorials/structured_data/time_series

        #print('Training Data:', self.__train_data[1], self.__train_data[0])
        #print('Training:')
        #print(np.average(self.__train_data[1]))
        evaluation = [np.nan, 0.0]
        previous = 10**9999
        count = 0
        #while (np.isnan(evaluation[0]) or evaluation[0] > 0.1) and (count < 1000):# and count < 10:
        #print('Iteration:', count, evaluation)
        if data is not None:
            result = self.__model.fit(
                #self.__train_ds,
                np.append(self.__train_data[0], data[0]),
                np.append(self.__train_data[1], data[1]),
                #self.__train_data,
                #self.__train_ds,
                validation_data=(self.__val_data[0], self.__val_data[1]),
                #validation_data=self.__val_ds,
                batch_size=32,
                epochs=epochs,
                callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True, verbose=1),# min_delta=0.0001,),
                        #tf.keras.callbacks.EarlyStopping(monitor='val_mae', patience=5, restore_best_weights=True, verbose=1, min_delta=0.0001,),
                        ],
                use_multiprocessing=self.__multiprocess,
                verbose=1,
            )
        else:
            result = self.__model.fit(
                #self.__train_ds,
                self.__train_data[0],
                self.__train_data[1],
                #self.__train_data,
                #self.__train_ds,
                validation_data=(self.__val_data[0], self.__val_data[1]),
                #validation_data=self.__val_ds,
                batch_size=32,
                epochs=epochs,
                callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True, verbose=1),# min_delta=0.0001,),
                        #tf.keras.callbacks.EarlyStopping(monitor='val_mae', patience=5, restore_best_weights=True, verbose=1, min_delta=0.0001,),
                        ],
                use_multiprocessing=self.__multiprocess,
                verbose=1,
            )
            #print(result['val_loss'])
        #print('Evaluating:')
        print('Evalutating '+self.__name+'...')
        evaluation = self.__model.evaluate(
            self.__test_data[0],
            self.__test_data[1],
            batch_size=32,
            verbose=1,
        )
        #print(evaluation, evaluation[0] > 0.1)
        count += 1
        # if previous < evaluation[0]:
        #     break
        # else:
        #     previous = evaluation[0]
        #self.__model.save(self.__modelFilename)
        #print('Predicting:')
        '''
        predicted = self.__model.predict(
            self.__test_data[0][:3],
            verbose=0,
        )
        '''
        #print(predicted.shape)
        #print(predicted[0])
        #print(np.average(self.__train_data[1]), np.std(self.__train_data[1]))
        #print('Acutal:')
        #print(self.__test_data[0][:3])
        #print(self.__test_data[1][:3])
        #return predicted
        '''
        if not (np.average(self.__train_data[1])-np.std(self.__train_data[1])*2*2 <= predicted[0] <= np.average(self.__train_data[1])+np.std(self.__train_data[1])*2*2):
            self.trainModel(epochs)
        else:
            for i in predicted:
                if i < 0:
                    self.trainModel(epochs)
                    break
        '''
        #self.saveModel()

    def makePredictions(self, url:str, startingPoint:float=time.time(), avgDist:int=60, quantity:int=60*60*12):
        """Generates predictions using a model.

        Args:
            url (str): The name of the URL and model to use.
            startingPoint (float, optional): The starting point, in seconds, for which the model should begin predicitng at. Defaults to time.time().
            avgDist (int, optional): The amount of time, in seconds, to exist between each point to predict over. Defaults to 60.
            quantity (int, optional): The ending point, in seconds, in time for which to stop predicting. Defaults to 60*60*12.

        Returns:
            np.array: A two dimensional numpy array containing the timestamp on the first axis and the predictions on the second axis.
        """
        self.setFilename(url)
        self.readModel()
        # https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing
        tempX = np.arange(startingPoint+avgDist, startingPoint+quantity, avgDist)
        timestamps, predictions = [], []
        print(str(time.ctime())+' - Predicting '+str(len(tempX))+' for '+self.__name+'...')
        for i, v in enumerate(tempX):
            predictions = np.append(predictions, self.__model.predict(
                [v],
                use_multiprocessing=self.__multiprocess,
                verbose=0
                ).flatten())
            timestamps = np.append(timestamps, v)
        #tempDF = pd.DataFrame({'timestamp':timestamps, 'latency':predictions,}, index=pd.to_datetime(timestamps, unit='s')).resample(self.__sampleRate).mean()
        #tempDF = tempDF.dropna(subset=['timestamp'])
        #tempDF = tempDF.dropna(subset=['latency'])
        #timestamps = tempDF[0].to_numpy()
        #predictions = tempDF[1].to_numpy()
        #self.graph(tempDF)
        print(str(time.ctime())+' - Completed predicting of '+str(len(tempX))+' units for '+self.__name+'...')
        return np.vstack((timestamps, predictions))

    def trainOnData(self, data:np.array, name:str='Unknown', sampleRate:str='15T', predictions:int=60*60*6, epochs:int=10*10**2, patience:int=100):
        """Trains the model using the data bgiven to it.

        Args:
            data (np.array): The data for which to train on.
            name (str, optional): The name of the model to use or create. Defaults to 'Unknown'.
            sampleRate (str, optional): The rate for which resampling will occur. Defaults to '15T'.
            predictions (int, optional): DEPRECATED The number of predictions to create. Defaults to 60*60*6.
            epochs (int, optional): The number of epochs to run the training for. Defaults to 10*10**2.
            patience (int, optional): The amount of patience to have during the training of the model. Defaults to 100.

        Returns:
            list[history]: DEPRECATED, A list contiaining the fit results and the evaluations results.
        """
        self.__sampleRate = sampleRate
        self.setFilename(name)
        self.setData(data)
        self.readModel()
        timerStart = time.time()
        print(str(time.ctime())+' - Training on '+self.__name+'...')
        result = self.__model.fit(
                self.__train_data[0],
                self.__train_data[1],
                validation_data=(self.__val_data[0], self.__val_data[1]),
                batch_size=32,
                epochs=epochs,
                callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True, verbose=1),],# min_delta=0.0001,),],
                use_multiprocessing=self.__multiprocess,
                verbose=0,
        )
        history = {}
        for i, v in enumerate(result.history):
            history[v] = np.min(result.history[v])
        print(str(time.ctime())+' - Results for '+self.__name+' '+str(history))#result.history['val_loss'])
        with open('gallery/'+self.__name+'.txt', 'a') as file:
            file.writelines('Training Results:\t'+'\t|\t'+str(time.ctime())+'\t|\t'+str(history)+'\n')
        evaluation = self.__model.evaluate(
            self.__test_data[0],
            self.__test_data[1],
            batch_size=32,
            verbose=0,
            use_multiprocessing=self.__multiprocess,
        )
        #for i, v in enumerate(evaluation)
        history2 = {}
        for i, v in enumerate(self.__model.metrics_names):
            history2[v] = evaluation[i]
        print(str(time.ctime())+' - Evaluation for '+self.__name+' '+str(history2))#result.history['val_loss'])
        with open('gallery/'+self.__name+'.txt', 'a') as file:
            file.writelines('Evaluation Results:\t'+'\t|\t'+str(time.ctime())+'\t|\t'+str(history2)+'\n')
        self.saveModel()
        print(str(time.ctime())+' - Training for '+self.__name+'_Predictor'+' completed in '+str(time.time()-timerStart)+' seconds.')
        return [history, history2]
    
    def predictOnData(self, data:np.array, name:str='Unknown', sampleRate:str='15T', predictions:int=60*60*6, epochs:int=10*10**2):
        """DEPRECATED, An all in one simplified function for giving the prediciton model data, training the model, and then makeing predictions.

        Args:
            data (list): The data to train and predict over.
            iterations (int, optional): The number of times to fit the model to the data. Defaults to 3.
            predictions (int, optional): The number of minutes to project over. Defaults to 180.
        Returns:
            list: A list of all the predictions for the next few data points
        """
        '''
        tempData = False
        print(len(data[0]))
        if self.isOdd(len(data[0])):
            tempDataX = np.delete(data[0], 0, None)
            tempDataY = np.delete(data[1], 0, None)
            self.__size = len(tempDataX)
            tempData = np.vstack((tempDataX, tempDataY))
        else:
            tempData = data
            self.__size = len(tempData[0])
        print(self.__size, self.isOdd(self.__size))
        '''
        self.__sampleRate = sampleRate
        self.setFilename(name)
        self.setData(data)
        self.readModel()
        timerStart = time.time()
        print('Training on '+self.__name+'...')
        predicted = self.trainModel(epochs)
        '''
        while not (np.average(self.__train_data[1])-np.std(self.__train_data[1])*2 <= predicted[0] <= np.average(self.__train_data[1])+np.std(self.__train_data[1])*2):
            predicted = self.trainModel(epochs)
            for i in predicted:
                if i < 0:
                    self.trainModel(epochs)
                    break
        '''
        self.saveModel()
        print('Predicting on '+self.__name+'...')
        prediction = self.predict(predictions)
        print('Training and Predicting for '+self.__name+' completed in '+str(time.time()-timerStart)+' seconds.')
        return prediction

    # def isOdd(self, number):
    #     k = 0
    #     while k<number:
    #         if 2*k+1 == number:
    #             return True
    #         elif 2*k == number:
    #             return False
    #         else:
    #             k +=1
    #     return None

def startPrediction(data:np.array, name:str='Unknown', sampleRate:str='15T', predictions:int=60*60*6, epochs:int=10*10**2):
    """The function to be called for training and generating sample predictions and graphs. Note: This is called as part of the multiprocessing seqeuence.

    Args:
        data (np.array): The data to train the model on.
        name (str, optional): The URL . Defaults to 'Unknown'.
        sampleRate (str, optional): _description_. Defaults to '15T'.
        predictions (int, optional): _description_. Defaults to 60*60*6.
        epochs (int, optional): _description_. Defaults to 10*10**2.
    """
    newPred = PredictionModel()
    #newPred.predictOnData(data, name, sampleRate, predictions, epochs)
    newPred.trainOnData(data=data, name=name, sampleRate=sampleRate, predictions=predictions, epochs=epochs, patience=epochs)
    temp = newPred.makePredictions(name)
    tempDF = pd.DataFrame({'timestamp':temp[0], 'latency':temp[1],}, index=pd.to_datetime(temp[0], unit='s')).resample(sampleRate).mean()
    newPred.graph(tempDF)