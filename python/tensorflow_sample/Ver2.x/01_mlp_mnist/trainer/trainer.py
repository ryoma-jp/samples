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
	def __init__(self, output_dir=None, model_file=None):
		# --- 出力ディレクトリ作成 ---
		self.output_dir = output_dir
		if (output_dir is not None):
			os.makedirs(output_dir, exist_ok=True)
		
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
# クラス; MLP学習モジュール
#---------------------------------
class TrainerMLP(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape, output_dir=None):
		# --- モデル構築 ---
		def _load_model(input_shape):
			model = keras.Sequential([
				keras.layers.Flatten(input_shape=input_shape),
				keras.layers.Dense(128, activation='relu'),
				keras.layers.Dense(10, activation='softmax')
			])
			
			model.summary()
			
			model.compile(
				optimizer='adam',
				loss = 'sparse_categorical_crossentropy',
				metrics=['accuracy'])
			
			return model
		
		# --- 基底クラスの初期化 ---
		super().__init__(output_dir)
		
		# --- モデル構築 ---
		self.model = _load_model(input_shape)
		if (self.output_dir is not None):
			keras.utils.plot_model(self.model, os.path.join(self.output_dir, 'plot_model.png'), show_shapes=True)
		
		return
	
