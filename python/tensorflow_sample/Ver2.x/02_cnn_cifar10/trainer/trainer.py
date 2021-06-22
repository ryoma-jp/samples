#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

import tensorflow as tf
from tensorflow import keras

#---------------------------------
# クラス; 学習モジュール基底クラス
#---------------------------------
class Trainer():
	# --- コンストラクタ ---
	def __init__(self, model_file=None):
		# --- モデル構築 ---
		def _load_model(model_file):
			if (model_file is not None):
				return None
			else:
				return None
		
		self.model = _load_model(model_file)
		return
	
	# --- 学習 ---
	def fit(self, x_train, y_train, x_test=None, y_test=None, epochs=5):
		# --- 学習 ---
		self.model.fit(x_train, y_train, epochs=epochs)
		
		# --- 学習結果を評価 ---
		if ((x_test is not None) and (y_test is not None)):
			test_loss, test_acc = self.model.evaluate(x_test, y_test, verbose=2)
			print('Test Accuracy: {}'.format(test_acc))
			print('Test Loss: {}'.format(test_loss))
		
		return
	
	# --- 推論 ---
	def predict(self, x_test):
		predictions = self.model.predict(x_test)
		return predictions
		
	# --- ラベルインデックス取得 ---
	def GetLabelIndex(self, label, onehot=True):
		if (onehot):
			label = np.argmax(label, axis=1)
		n_category = max(label)+1
		
		return np.array([np.arange(len(label))[label==i] for i in range(n_category)])

#---------------------------------
# クラス; CNN学習モジュール
#---------------------------------
class TrainerCNN(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape):
	# --- モデル構築 ---
		def _load_model(input_shape):
			model = keras.models.Sequential()
			model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
			model.add(keras.layers.MaxPooling2D((2, 2)))
			model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
			model.add(keras.layers.MaxPooling2D((2, 2)))
			model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
			model.add(keras.layers.MaxPooling2D((2, 2)))
			model.add(keras.layers.Flatten(input_shape=input_shape))
			model.add(keras.layers.Dense(64, activation='relu'))
			model.add(keras.layers.Dense(10, activation='softmax'))
			
			model.summary()
			
			model.compile(
				optimizer='adam',
				loss = 'sparse_categorical_crossentropy',
				metrics=['accuracy'])
			
			return model
		
		# --- 基底クラスの初期化 ---
		super().__init__()
		
		# --- モデル構築 ---
		self.model = _load_model(input_shape)
		
		return
	

#---------------------------------
# クラス; MLP学習モジュール
#---------------------------------
class TrainerMLP(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape):
	# --- モデル構築 ---
		def _load_model(input_shape):
			model = keras.models.Sequential()
			model.add(keras.layers.Flatten(input_shape=input_shape))
			model.add(keras.layers.Dense(128, activation='relu'))
			model.add(keras.layers.Dense(10, activation='softmax'))
			
			model.summary()
			
			model.compile(
				optimizer='adam',
				loss = 'sparse_categorical_crossentropy',
				metrics=['accuracy'])
			
			return model
		
		# --- 基底クラスの初期化 ---
		super().__init__()
		
		# --- モデル構築 ---
		self.model = _load_model(input_shape)
		
		return
	
