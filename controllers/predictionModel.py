# Created by Anthony Castillo

#TENSORFLOW INSTALL 
"""
FOR WINDOWS: powershell => run as administer => run this command
___________________________________________________________________
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
___________________________________________________________________
After that go back to terminal:
___________________________________________________________________
pip show tensorflow
pip install --upgrade tensorflow
___________________________________________________________________
"""
#PSUTIL Install
"""
pip install psutil
"""



import time
import datetime
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib as plt
class PredictionModel():
    """_summary_
    """
    def __init__(self):
        self.__train_data = False
        self.__val_data = False
        self.__test_data = False
        self.__model = False
        self.__size = 0
        self.__train_ds = False
        self.__val_ds = False
        self.__test_ds = False
        self.__modelFilename = 'predictionModel.keras'

    def __del__(self):
        """_summary_
        """
        del self.__train_data, self.__val_data, self.__test_data, self.__model, self.__modelFilename, self.__size, self.__train_ds, self.__val_ds, self.__test_ds

    def requestData(self, request): # Not Used, data should be passed to this class instead
        """_summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.__requestQ.put(request)
        time.sleep(0.1)
        initialDataID = False
        while self.__dataQ.empty() != True:
            newData = self.__dataQ.get()
            print(newData)
            if newData['id'] == initialDataID:
                self.__requestQ.put(request)
                time.sleep(0.1) #import time
                initialDataID = False
            elif initialDataID == False:
                initialDataID = newData['id']
            if newData['id'] == request['id']:
                if newData['data'] is not False:
                    return newData
            else:
                self.__dataQ.put(newData)

    def createModel(self):
        """WIP
        """
        self.__model = tf.keras.Sequential([
            #tf.keras.layers.Lambda(lambda x: x[:, -11:, :]),
            #tf.keras.Input(shape=(int(self.__size*0.7))), #, int(self.__size*0.7))),
            #tf.keras.layers.Reshape((int(self.__size*0.7*0.5), 2), input_shape=(int(self.__size*0.7),)),# dtype=tf.float32), # int(int(self.__size*0.7)//(self.__size*0.7*0.5))
            #tf.keras.layers.Dense(256, activation='LeakyReLU'),# input_shape=(32,)),#(self.__size*0.7), 2)),
            tf.keras.layers.Dense(256),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(128, activation='gelu'), #input_shape=(int(self.__size*0.7), 2)),
            #tf.keras.layers.Dense(128),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(2, activation='softmax'),# input_shape=(int(self.__size*0.7), 2))
            tf.keras.layers.Dense(1)
        ])
        #loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
        
        self.__model.compile(
            optimizer='adam',#tf.keras.optimizers.Adam(learning_rate=0.001), 
            loss='mse', 
            metrics=['accuracy', tf.keras.metrics.MeanAbsoluteError()]#[tf.keras.metrics.SparseCategoricalAccuracy()]
            )#'sparse_categorical_crossentropy')#'mse')#loss_fn,)
        #print(len(self.__model.weights))
        #print(self.__model.get_config())
        self.__model.build(input_shape=(32, 1,))
        self.__model.summary()
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
            self.__model.summary()
            self.__model.save(self.__modelFilename)
        except:
            print('Could not save prediction model.')

    def readModel(self):
        """Reads a model from file using the name provided in self.__modelFilename
        """
        try:
            self.__model = tf.keras.models.load_model(self.__modelFilename)
            self.__model.summary()
        except:
            self.createModel()

    def setFilename(self, name:str):
        """Changes the file name that the model gets saved as. Additionally creates a new model and then saves it to the new file.

        Args:
            name (str): The name to change the model's file
        """
        self.__modelFilename = 'predictionModels/'+name+'.keras'
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
        #tempMean = 
        #print(tempMean, tempMean**2)
        print(len(tempDataX))
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
        print(np.nanmean(tempDataY), np.nanmean(tempDataY)**2)

        self.__size = len(tempDataX)
        #print('Starting Size: ', self.__size, int(self.__size*0.7))
        while int(self.__size*0.7)%2 != 0:#self.isOdd(int(self.__size*0.7)): # 
            tempDataX = np.delete(tempDataX, 0, None)
            tempDataY = np.delete(tempDataY, 0, None)
            self.__size = len(tempDataX)
            print(self.__size, int(self.__size*0.7))
        #print('Ending Size: ', self.__size, int(self.__size*0.7))
        #tempData = np.vstack((tempDataX, tempDataY))
        #print(tempDataY*100)
        #print(np.nanmean(tempDataY), np.nanstd(tempDataY))
        #print(tempDataY.mean(), tempDataY.std())
        timestampData = tempDataX
        latencyData = tempDataY

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
        
        # print('Training Data:\n', self.__train_data)
        # print('Validation Data:\n', self.__val_data)
        # print('Test Data:\n', self.__test_data)
        # print('Length: ', self.__size, '70%: ', int(self.__size*0.7), ' ', 'Mean: ', train_mean, ' ', 'STD: ', train_std)

        # Normalizing data
        #self.__train_data[1] = (self.__train_data[1] - train_mean) / train_std
        #self.__val_data[1] = (self.__val_data[1] - train_mean) / train_std
        #self.__test_data[1] = (self.__test_data[1] - train_mean) / train_std

        #print(self.__train_data[0][0])
        #print(self.__train_data[0][1])
        #print(self.__train_data[0][-1])

        temptemptemp = np.empty(1)
        #print(self.__size, len(train_dataX)-1)
        for i in range(0, len(train_dataX)-2):
            temptemptemp = np.append(temptemptemp, train_dataX[i+1]-train_dataX[i])
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

    def clearModel(self):
        """Resets the model back to a skeleton model (i.e., no training.)
        """
        self.__model = False
        self.createModel()
    
    def predict(self, quantity:int=60*60*24):
        """Projects the future for the current data using the fitted model.

        Args:
            quantity (int, optional): The number of minutes to project over. Defaults to 60*3.

        Returns:
            list: A list of all the predictions
        """
        # https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing
        
        temp = np.arange(self.__train_data[0][-1], self.__train_data[0][-1]+quantity, self.__avgDist)
        #print(temp)
        predictions = self.__model.predict(temp)#tf.expand_dims(self.__data, axis=0))
        outputDF = pd.DataFrame(predictions) # [{'data0'}, {'data1'}, {'data2'}, {'etc.'}, {'data#quantity-1#'}]
        #outputDF.add()
        #plt.pyplot.plot(data[0], data[1], 'o', label='Original Data')
        tempY = outputDF[0].to_numpy()
        #print(outputDF)
        plt.pyplot.plot(self.__train_data[0], self.__train_data[1], 'o', alpha=1.0, label='Normalized Data')
        plt.pyplot.plot(temp, tempY, 'o', alpha=0.5, label='Predictions')

        plt.pyplot.legend()
        plt.pyplot.show()

        return np.vstack(temp, tempY)

    def trainModel(self, epochs:int = 3):
        """Trians the model on the data given using the 

        Args:
            iterations (int, optional): The number of time the model will be fitted to the data. Defaults to 3.
        """
        #https://www.tensorflow.org/tutorials/structured_data/time_series

        #print('Training Data:', self.__train_data[1], self.__train_data[0])
        print('Training:')
        evaluation = [np.nan, 0.0]
        count = 0
        while (np.isnan(evaluation[0]) or evaluation[0] > 0.001) and count < 10:
            print(count)
            for i in range(epochs):
                result = self.__model.fit(
                    #self.__train_ds,
                    self.__train_data[0],
                    self.__train_data[1],
                    #self.__train_data,
                    #self.__train_ds,
                    validation_data=(self.__val_data[0], self.__val_data[1]),
                    #validation_data=self.__val_ds,
                    batch_size=32,
                    epochs=1
                )
            print('Evaluating:')
            evaluation = self.__model.evaluate(
                self.__test_data[0],
                self.__test_data[1],
                batch_size=32
            )
            print(evaluation)
            count += 1
        print('Prediction:')
        predicted = self.__model.predict(
            self.__test_data[0][:3]
        )
        print(predicted)
        print('Acutal:')
        print(self.__test_data[0][:3])
        print(self.__test_data[1][:3])
        self.saveModel()

    def predictOnData(self, data:np.array, name:str='Unknown', epochs:int=3, predictions:int=60*60*6):
        """An all in one simplified function for giving the prediciton model data, training the model, and then makeing predictions.

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
        self.setFilename(name)
        self.setData(data)
        self.readModel()
        self.trainModel(epochs)
        return self.predict(predictions)

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