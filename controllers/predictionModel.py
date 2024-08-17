# Created by Anthony Castillo

import time
import logging
from pathlib import Path
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from controllers.windowGenerator import WindowGenerator
from controllers.residualWrapper import ResidualWrapper
class PredictionModel():
    """This class is designed to create a model, train the model on data, make future predictions on data, generate (temporary) graphs on and return those predictions. NOTE: This is still a WIP and is subject to change. In fact, a lot of this will be removed and possibly refactored.
    Created by Anthony Castillo.
    """
    def __init__(self):
        """Initializes most variables to False
        """
        self.__currTime = None
        self._configureDirectories()
        self.__model = False
        self.__name = 'unknown'
        self.__modelPath = 'predictionModels/unknown.keras'
        self.__modelCheckpointPath = 'predictionModels/checkpoints/unknown.keras'

        self.__data = None
        self.__window = None
        self.__num_features = 0
        self.__data_std = 0

        self.__multiprocess = True
        tf.keras.backend.set_floatx('float64')
    # end __init__

    def __del__(self):
        """Deletes variables
        """
        del self.__train_data, self.__val_data, self.__test_data, self.__model, self.__modelFilename, self.__size, self.__train_ds, self.__val_ds, self.__test_ds, self.__avgDist, self.__sampleRate, self.__name, self.__originalDataCleaned, self.__multiprocess
    # end __del__

    def _configureFilename(self, timeData):
        currTimeString = str(timeData[0])
        if len(str(timeData[1])) == 1:
            currTimeString += '0'+str(timeData[1])
        else:
            currTimeString += str(timeData[1])
        if len(str(timeData[2])) == 1:
            currTimeString += '0'+str(timeData[2])
        else:
            currTimeString += str(timeData[2])
        return currTimeString
    
    def _setLogger(self):
        self.__currTime = time.localtime()
        logging.basicConfig(filename='./logs/'+self._configureFilename(self.__currTime)+'.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(time.ctime()+' - Initializing...')
        logging.info(time.ctime()+' - Saving log to runtime_'+self._configureFilename(self.__currTime)+'.log')
        print(time.ctime()+' - Saving log to runtime_'+self._configureFilename(self.__currTime)+'.log')
    # end _setLogger

    def _configureDirectories(self):
        if not Path('./logs').is_dir():
            Path('./logs').mkdir()
            print(time.ctime()+' - ./logs directory has been created.')
        self._setLogger()
        if not Path('./graphs').is_dir():
            Path('./graphs').mkdir()
            logging.info(time.ctime()+' - ./graphs directory has been created.')
        if not Path('./predictionModels').is_dir():
            Path('./predictionModels').mkdir()
            logging.info(time.ctime()+' - ./predictionModels directory has been created.')
        if not Path('./predictionModels/checkpoints').is_dir():
            Path('./predictionModels/checkpoints').mkdir()
            logging.info(time.ctime()+' - ./predictionModels/checkpoints directory has been created.')
    # end configureDirectories

    def setName(self, name:str):
        """Changes the file name that the model gets saved as. Additionally creates a new model and then saves it to the new file.

        Args:
            name (str): The name to change the model's file
        """
        self.__name = name
        self.__modelPath = 'predictionModels/'+name+'.keras'
        self.__modelCheckpointPath = 'predictionModels/checkpoints/'+name+'.keras'
        logging.info(time.ctime()+' - Name has been set to '+str(self.__name))
    # end setFilename

    def getName(self):
        """Returns the name of the file that the model is saved in

        Returns:
            str: The name of the file the model is saved to
        """
        return self.__name
    # end getFilename

    def clearModel(self):
        """Resets the model back to a skeleton model (i.e., no training.)
        """
        self.__model = False
        self.__name = 'unknown'
        self.__modelPath = 'predictionModels/unknown.keras'
        self.__modelCheckpointPath = 'predictionModels/checkpoints/unknown.keras'
        self.createModel()
        logging.info(time.ctime()+' - Model has been cleared.')
    # end clearModel

    def readModel(self):
        """Reads a model from file using the name provided in self.__modelFilename
        """
        try: # Model First
            self.__model = tf.keras.models.load_model(self.__modelPath)
            logging.info(time.ctime()+' - Successfully read model from '+str(self.__modelPath))
            #self.__model.summary()
        except Exception as e:
            try: # Checkpoint Second
                logging.info(time.ctime()+' - '+str(e))
                self.__model = tf.keras.models.load_model(self.__modelCheckpointPath)
                logging.info(time.ctime()+' - Successfully read model from '+str(self.__modelCheckpointPath))
            except Exception as e: # Create new model
                logging.info(time.ctime()+' - '+str(e))
                logging.info(time.ctime()+' - Creating new model...')
                self.createModel()
    # end readModel

    def createModel(self):
        """Creates, builds, and assigns a new model for this class to use.
        """
        self.__model = ResidualWrapper(tf.keras.Sequential([
            tf.keras.layers.LSTM(32, return_sequences=True),
            tf.keras.layers.Dense(self.__num_features, kernel_initializer=tf.initializers.zeros()),
        ]))

        self.__model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=[tf.keras.metrics.MeanAbsoluteError()],
        )
        logging.info(time.ctime()+' - Model '+str(self.__name)+' has been created.')
    # end createModel

    def saveModel(self):
        """Saves the model to a file using the name provided in self.__modelFilename
        """
        try:
            #self.__model.summary()
            self.__model.save(self.__modelPath)
            logging.info(time.ctime()+' - Model '+str(self.__name)+' has been saved to '+str(self.__modelPath))
        except:
            logging.info(time.ctime()+' - Could not save '+str(self.__modelFilename))
            print(str(time.ctime())+' - Could not save '+str(self.__modelFilename))
    # end saveModel

    def clearData(self):
        """Empties the data that is currently stored by the model
        """
        self.__data = None
        self.__window = None
        self.__num_features = 0
        self.__data_std = 0
        logging.info(time.ctime()+' - Data has been cleared.')
    # end clearData

    def setData(self, data:np.array, conv_width, predictions,):
        """Clears out the old data and then sets the new data in the class.

        Args:
            data (list): A list of dictionaries to work with (i.e., [{data0}, {data1}, {data2}])
        """
        # tempDataX = data[0] # Timestamp
        # tempDataY = data[1]*100 # Latency
        self.clearData()

        self.__data = pd.Dataframe(
            data=data,
            index=data[0]
        )

        # Creating a day/night time frequency
        timestamp_s = self.__datetime.map(pd.Timestamp.timestamp)
        day = 24*60*60
        newColumns = pd.DataFrame({
            'Day_Sin': np.sin(timestamp_s * (2 * np.pi / day)),
            'Day_Cos': np.cos(timestamp_s * (2 * np.pi / day)),
            })
        self.__data = pd.concat([self.__data, newColumns], axis=1)
        
        # Normalizing Data
        n=len(self.__data)
        train_df = self.__data[0:int(n*0.7)]
        val_df = self.__data[int(n*0.7):int(n*0.9)]
        test_df = self.__data[int(n*0.9):]
        self.__num_features = self.__data.shape[1]
        train_mean = self.__train_df.mean()
        train_std = self.__train_df.std()
        self.__data_std = (self.__data - train_mean) / train_std
        
        # Create Window
        self.__window = WindowGenerator(
            input_width=conv_width,
            label_width=predictions,
            shift=1,
            train_df=train_df,
            val_df=val_df,
            test_df=test_df,
        )
        logging.info(time.ctime()+' - Data has been set, normalized, and a new window has been created.')
    # end setData

    def trainModel(self, maxEpochs:int=10*10**2):
        """DEPRECATED, Trians the model on the data given using the 

        Args:
            iterations (int, optional): The number of time the model will be fitted to the data. Defaults to 3.
        """
        #https://www.tensorflow.org/tutorials/structured_data/time_series
        
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            verbose=1,
            patience=self.__num_features*3,
            mode='min',
        )

        auto_save = tf.keras.callbacks.ModelCheckpoint(
            filepath='',
            monitor='val_loss',
            verbose=1,
            save_best_only=True,
            mode='auto',
            save_freq='epoch',
        )        

        history = self.__model.fit(
            self.__data.getWindowTrainData(),
            epochs=maxEpochs,
            validation_data=self.__data.getWindowTrainValidation(),
            callbacks=[early_stopping, auto_save],
        )
        logging.info(time.ctime()+' - Finished training model '+str(self.__name)+' with '+str(history.history['loss'])+' after '+str(history.params['epochs'])+' epochs')
        return history
    # end trainModel

    def evaluateModel(self):
        performance = {}
        performance['validationSet'] = self.__model.evaluate(self.__window.getData()[1], verbose=0, return_dict=True)
        performance['testSet'] = self.__model.evaluate(self.__window.getData()[3], werbose=0, return_dict=True)
        x = np.arage(len(performance))
        width = 0.3
        metric_name = 'mean_absolute_error'
        plt.figure(figsize=(16,9))
        plt.ylabel(metric_name+' of '+self.__name)
        plt.bar(x-0.17, performance['validationSet'][metric_name], width, label='Validation Set')
        plt.bar(x+0.17, performance['testSet'][metric_name], width, label='Test Set')
        plt.gcf().suptitle(self.__name+' Model Performance')
        plt.xticks(ticks=x, label=self.__name, rotation=60)
        _ = plt.legend()
        plt.savefig('graphs/performance_'+self.__name+'.png')
        self.__window.plot(self.__model)
        plt.savefig('graphs/'+self.__name+'.png')
        logging.info(time.ctime()+' - Created and saved performance_'+self.__name+'.png and '+self.__name+'.png to ./graphs/')
    # end evaluateModel

    def predictModel(self, input):
        predictions = self.__model.predict(input)
        logging.info(time.ctime()+' - Made '+len(predictions)+' predictions with model '+self.__name)
        return predictions
    # end predictModel