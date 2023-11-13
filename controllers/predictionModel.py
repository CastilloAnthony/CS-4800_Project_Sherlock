# Created by Anthony Castillo
import time
import datetime
import tensorflow as tf
import pandas as pd
import numpy as np
class PredictionModel():
    """_summary_
    """
    def __init__(self):
        self.__data = False
        self.__model = False
        self.__modelFilename = 'predictionModel.keras'
        self.__size = 0

    def __del__(self):
        """_summary_
        """
        del self.__data, self.__model

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
            tf.keras.layers.Dense(8, activation='relu', input_shape=(int(self.__size*0.7),)),
            tf.keras.layers.Dense(4, activation='relu', input_shape=(int(self.__size*0.7),)),
            tf.keras.layers.Dense(1, activation='relu', input_shape=(int(self.__size*0.7),))
        ])
        #loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
        self.__model.compile(optimizer='adam', loss='mse')#'sparse_categorical_crossentropy')#'mse')#loss_fn,)
        #print(len(self.__model.weights))
        #self.__model.summary()
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
            self.__modle.save(self.__modelFilename)
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
        self.__modelFilename = name
        self.createModel()
        self.saveModel()

    def getFilename(self):
        """Returns the name of the file that the model is saved in

        Returns:
            str: The name of the file the model is saved to
        """
        return self.__modelFilename
    
    def setData(self, data:list):
        """Clears out the old data and then sets the new data in the class.

        Args:
            data (list): A list of dictionaries to work with (i.e., [{data0}, {data1}, {data2}])
        """
        self.clearData()
        self.__data = data

    def clearData(self):
        """Empties the data that is currently stored by the model
        """
        self.__data = False

    def clearModel(self):
        """Resets the model back to a skeleton model (i.e., no training.)
        """
        self.__model = False
        self.createModel()
    
    def predict(self, quantity:int=60*3):
        """Projects the future for the current data using the fitted model.

        Args:
            quantity (int, optional): The number of minutes to project over. Defaults to 60*3.

        Returns:
            list: A list of all the predictions
        """
        # https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing
        
        predictions = self.__model.predict([np.arange(0, quantity)])#tf.expand_dims(self.__data, axis=0))
        outputDF = pd.DataFrame(predictions) # [{'data0'}, {'data1'}, {'data2'}, {'etc.'}, {'data#quantity-1#'}]
        #outputDF.add()
        return outputDF

    def trainModel(self, iterations:int = 3):
        """Trians the model on the data given using the 

        Args:
            iterations (int, optional): The number of time the model will be fitted to the data. Defaults to 3.
        """
        #https://www.tensorflow.org/tutorials/structured_data/time_series
        batch_size = 32
        n = self.__data[0].size
        #print(n, len(self.__data[0]), self.__data[0].size)
        print(n)
        #train_data = self.__data[0:int(n*0.)]
        #val_data = self.__data[int(n*0.7):int(n*0.9)]
        #test_data = self.__data[int(n*0.9):]
    
        train_dataX = self.__data[0][0:int(n*0.7)]
        train_dataY = self.__data[1][0:int(n*0.7)]
        val_dataX = self.__data[0][int(n*0.7):int(n*0.9)]
        val_dataY = self.__data[1][int(n*0.7):int(n*0.9)]
        test_dataX = self.__data[0][int(n*0.9):]
        test_dataY = self.__data[1][int(n*0.9):]

        train_data = np.vstack((train_dataX, train_dataY))
        val_data = np.vstack((val_dataX, val_dataY))
        test_data = np.vstack((test_dataX, test_dataY))
        
        #print(train_data)
        #print(val_data)
        #print(test_data)
        train_mean = train_data[1].mean()
        train_std = train_data[1].std()
        print('Training Data:\n', train_data)
        print('Validation Data:\n', val_data)
        print('Test Data:\n', test_data)
        print('Length: ', n, int(n*0.7))
        print('Length: ', str(n), ' ', 'Mean: ', train_mean, ' ', 'STD: ', train_std)
        train_data[1] = (train_data[1] - train_mean) / train_std
        val_data[1] = (val_data[1] - train_mean) / train_std
        test_data[1] = (test_data[1] - train_mean) / train_std
        '''
        train_ds = tf.keras.utils.timeseries_dataset_from_array(
            data=train_data,
            targets=None,
            sequence_length=train_data.size+60*3,
            sequence_stride=1,
            shuffle=False,
            batch_size=32
        )
        val_ds = tf.keras.utils.timeseries_dataset_from_array(
            data=val_data,
            targets=None,
            sequence_length=val_data.size+60*3,
            sequence_stride=1,
            shuffle=False,
            batch_size=32
        )
        '''
        #print(train_ds, val_ds)
        #train_latency = self.__data['latency'] - train_mean / train_std
        #val_latency = tf.keras.utils.timeseries_dataset_from_array()
        
        for i in range(iterations):
            self.__model.fit(
                train_data[0],
                train_data[1],
                validation_data=(val_data[0], val_data[1]),
                epochs=1
                )
            #self.__model.fit(self.__data['latency'], self.__data['timestamp'], batch_size=32)
        self.saveModel()

    def predictOnData(self, data:list, iterations:int=3, predictions:int=180):
        """An all in one simplified function for giving the prediciton model data, training the model, and then makeing predictions.

        Args:
            data (list): The data to train and predict over.
            iterations (int, optional): The number of times to fit the model to the data. Defaults to 3.
            predictions (int, optional): The number of minutes to project over. Defaults to 180.
        Returns:
            list: A list of all the predictions for the next few data points
        """
        self.__size = len(data[0])
        self.readModel()
        self.setData(data)
        self.trainModel(iterations)
        return self.predict(predictions)
