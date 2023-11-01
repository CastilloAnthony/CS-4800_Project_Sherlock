import time
import tensorflow as tf

class PredictionModel():
    def __init__(self):
        self.__data = False
        self.__model = False

    def __del__(self):
        del self.__data, self.__model

    def requestData(self, request): # Not Used
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
        OUT_STEPS, num_features = 1
        self.__model = tf.keras.Sequential([
            tf.keras.layers.Lambda(lambda x: x[:, -11:, :]),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(OUT_STEPS*num_features, kernel_initializer=tf.initializaers.zeros()),
            tf.keras.layers.Reshape([OUT_STEPS, num_features])
        ])
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

    def setData(self, data):
        self.__data = data

    def clearData(self):
        self.__data = False

    def predict(self):
        pass

    def trainModel(self):
        pass