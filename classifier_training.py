from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from tkinter import filedialog as fd
from skimage.exposure import rescale_intensity
import pickle
import numpy as np

class ModelTrainer(object):

    def __init__(self):
        self.X = None
        self.y = None
        self.X_test = None
        self.y_test = None
        self.model = None
        self.eval = None

    def load_data(self, X_path=None, y_path=None):

        if X_path is None:
            print("Load X")
            X_path = fd.askopenfilename()

        if y_path is None:
            print("Load y")
            y_path = fd.askopenfilename()

        self.X = np.array(pickle.load(open(X_path, "rb")))
        #self.X = np.array([np.concatenate((rescale_intensity(x[0]), rescale_intensity(x[1])), axis=1) for x in self.X])
        print(self.X.shape)
        self.y = np.array(pickle.load(open(y_path, "rb")))
        self.y = [int(i)-1 for i in self.y]

    def process_data(self, max_x, max_y):
        self.X = np.array(list(self.X)).reshape(-1, max_x, max_y, 1)

    def create_model(self):
        self.model = Sequential()
        self.model.add(Conv2D(16, (3, 3),padding='same', input_shape=self.X.shape[1:]))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(16, (3, 3), padding='same'))
        self.model.add(Activation('relu'))

        self.model.add(Conv2D(16, (3, 3), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3), padding='same'))
        self.model.add(Activation('relu'))

        self.model.add(Flatten())

        self.model.add(Dense(100))
        self.model.add(Activation('relu'))

        self.model.add(Dense(3))
        self.model.add(Activation('softmax'))
        self.model.summary()

    def compile_model(self):
        self.model.compile(loss='sparse_categorical_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

    def train_model(self, val_split=0.3, n_epochs=50, n_batch_size=1000):
        tbCallBack = TensorBoard(log_dir="./Graph", histogram_freq=0,
                                 write_graph=True, write_images=True)
        self.model.fit(self.X, self.y, validation_split=val_split,
                       epochs=n_epochs, batch_size=n_batch_size,
                       verbose=1,
                       callbacks=[tbCallBack])

    def save_model(self, path=None):
        if path is None:
            path = fd.asksaveasfilename()(title="Save Model")
        self.model.save(path)

    def run_trainer(self, _X_path, _y_path):
        self.load_data(X_path=_X_path, y_path=_y_path)
        self.process_data(100, 200)
        self.create_model()
        self.compile_model()
        self.train_model()

