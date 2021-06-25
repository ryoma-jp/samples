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
# クラス; ResNet学習モジュール
#---------------------------------
class TrainerResNet(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape, output_dir=None):
		# --- Residual Block ---
		#  * アプリケーションからkeras.applications.resnet.ResNetにアクセスできない為，
		#    必要なモジュールをTensorFlow公式からコピー
		#      https://github.com/tensorflow/tensorflow/blob/v2.5.0/tensorflow/python/keras/applications/resnet.py#L212
		def block1(x, filters, kernel_size=3, stride=1, conv_shortcut=True, name=None):
			bn_axis = 3
			
			if conv_shortcut:
				shortcut = keras.layers.Conv2D(4 * filters, 1, strides=stride, name=name + '_0_conv')(x)
				shortcut = keras.layers.BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name=name + '_0_bn')(shortcut)
			else:
				shortcut = x

			x = keras.layers.Conv2D(filters, 1, strides=stride, name=name + '_1_conv')(x)
			x = keras.layers.BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name=name + '_1_bn')(x)
			x = keras.layers.Activation('relu', name=name + '_1_relu')(x)

			x = keras.layers.Conv2D(filters, kernel_size, padding='SAME', name=name + '_2_conv')(x)
			x = keras.layers.BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name=name + '_2_bn')(x)
			x = keras.layers.Activation('relu', name=name + '_2_relu')(x)

			x = keras.layers.Conv2D(4 * filters, 1, name=name + '_3_conv')(x)
			x = keras.layers.BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name=name + '_3_bn')(x)

			x = keras.layers.Add(name=name + '_add')([shortcut, x])
			x = keras.layers.Activation('relu', name=name + '_out')(x)
			return x
		
		# --- Residual Block stack ---
		#  * アプリケーションからkeras.applications.resnet.ResNetにアクセスできない為，
		#    必要なモジュールをTensorFlow公式からコピー
		#      https://github.com/tensorflow/tensorflow/blob/v2.5.0/tensorflow/python/keras/applications/resnet.py#L257
		def stack1(x, filters, blocks, stride1=2, name=None):
			x = block1(x, filters, stride=stride1, name=name + '_block1')
			for i in range(2, blocks + 1):
				x = block1(x, filters, conv_shortcut=False, name=name + '_block' + str(i))
			return x
		
		# --- モデル構築 ---
		#   0: original ResNet50, 1: custom ResNet50
		def _load_model_resnet50(input_shape, classes, dbg_mode=1):
			if (dbg_mode == 0):
				model = keras.applications.resnet50.ResNet50()
			elif (dbg_mode == 1):
				def stack_fn(x):
					x = stack1(x, 64, 3, stride1=1, name='conv2')
					x = stack1(x, 128, 4, name='conv3')
					x = stack1(x, 256, 6, name='conv4')
					return stack1(x, 512, 3, name='conv5')
				
				input = keras.layers.Input(shape=[224, 224, 3])
				bn_axis = 3
				
				x = keras.layers.ZeroPadding2D(padding=((3, 3), (3, 3)), name='conv1_pad')(input)
				x = keras.layers.Conv2D(64, 7, strides=2, use_bias=True, name='conv1_conv')(x)

				x = keras.layers.BatchNormalization(axis=bn_axis, epsilon=1.001e-5, name='conv1_bn')(x)
				x = keras.layers.Activation('relu', name='conv1_relu')(x)

				x = keras.layers.ZeroPadding2D(padding=((1, 1), (1, 1)), name='pool1_pad')(x)
				x = keras.layers.MaxPooling2D(3, strides=2, name='pool1_pool')(x)

				x = stack_fn(x)

				x = keras.layers.GlobalAveragePooling2D(name='avg_pool')(x)
				x = keras.layers.Dense(classes, activation='softmax', name='predictions')(x)
				
				model = keras.models.Model(input, x)
				
			model.summary()
			
			return model
		
		# --- 基底クラスの初期化 ---
		super().__init__(output_dir)
		
		# --- モデル構築 ---
		self.model = _load_model_resnet50(input_shape, 1000)
		if (self.output_dir is not None):
			keras.utils.plot_model(self.model, os.path.join(self.output_dir, 'plot_model.png'), show_shapes=True)
		
		return
	
#---------------------------------
# クラス; CNN学習モジュール
#---------------------------------
class TrainerCNN(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape, output_dir=None):
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
		super().__init__(output_dir)
		
		# --- モデル構築 ---
		self.model = _load_model(input_shape)
		if (self.output_dir is not None):
			keras.utils.plot_model(self.model, os.path.join(self.output_dir, 'plot_model.png'), show_shapes=True)
		
		return
	

#---------------------------------
# クラス; MLP学習モジュール
#---------------------------------
class TrainerMLP(Trainer):
	# --- コンストラクタ ---
	def __init__(self, input_shape, output_dir=None):
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
		super().__init__(output_dir)
		
		# --- モデル構築 ---
		self.model = _load_model(input_shape)
		if (self.output_dir is not None):
			keras.utils.plot_model(self.model, os.path.join(self.output_dir, 'plot_model.png'), show_shapes=True)
		
		return
	


#---------------------------------
# メイン処理; Trainerモジュールテスト
#---------------------------------
def main():
	def _argparse():
		parser = argparse.ArgumentParser(description='Trainerモジュールテスト\n'
					'  * test_mode=\'ResNet\': ResNetのモデル構造確認(ResNet50の構造をTensorFlow公開モデルと比較)',
					formatter_class=argparse.RawTextHelpFormatter)

		# --- 引数を追加 ---
		parser.add_argument('--test_mode', dest='test_mode', type=str, default='ResNet', required=False, \
				help='テストモード(ResNet)')

		args = parser.parse_args()
		return args

	# --- 引数処理 ---
	args = _argparse()
	print(args.test_mode)
	
	# --- モジュールテスト ---
	if (args.test_mode == 'ResNet'):
		trainer = TrainerResNet([224, 224, 3], output_dir=None)
	else:
		print('[ERROR] Unknown test_mode: {}'.format(args.test_mode))
	
	return

	
if __name__ == '__main__':
	main()
