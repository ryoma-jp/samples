#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
from sklearn.model_selection import train_test_split

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def trainer(train_images, train_labels):
	x = train_images.astype(np.float32) / 255
	y = train_labels
	
	input_shape = x.shape[1:]
	n_class = y.shape[1]
	
	# --- separate train and validation ---
	x_train, x_val, y_train, y_val = train_test_split(x, y, random_state=42, test_size=0.1)
	
	# --- Build model ---
	model = Sequential()
	model.add(Conv2D(filters=16, kernel_size=(5, 5), activation="relu", input_shape=input_shape))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(filters=64, kernel_size=(5, 5), activation="relu"))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(64, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(n_class, activation='sigmoid'))
	model.summary()
	
	# --- train ---
	model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
	model.fit(x_train, y_train, epochs=100, validation_data=(x_val, y_val), batch_size=64)
	
	return


