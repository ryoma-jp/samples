#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import io
import os
import argparse
import pandas as pd

from data_loader.data_loader import DataLoaderMNIST
from data_loader.data_loader import DataLoaderCIFAR10

from trainer.trainer import TrainerMLP, TrainerCNN, TrainerResNet

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='TensorFlowの学習実装サンプル\n'
													'  * No.01: MNISTデータセットを用いた全結合NN学習サンプル\n'
													'  * No.02: CIFAR-10データセットを用いたCNN学習サンプル\n'
													'  * No.03: CIFAR-10データセットを用いたResNet学習サンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--data_type', dest='data_type', type=str, default='CIFAR-10', required=False, \
			help='データ種別(MNIST, CIFAR-10)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')
	parser.add_argument('--model_type', dest='model_type', type=str, default='ResNet', required=False, \
			help='モデル種別(MLP, SimpleCNN, SimpleResNet)')
	parser.add_argument('--data_augmentation', dest='data_augmentation', type=str, default=None, required=False, \
			help='Data Augmentationパラメータをカンマ区切りで指定\n'
					'  rotation_range,width_shift_range,height_shift_range,horizontal_flip\n'
					'    rotation_range: 回転範囲をdeg単位で指定\n'
					'    width_shift_range: 水平方向のシフト範囲を画像横幅に対する割合で指定\n'
					'    height_shift_range: 垂直方向のシフト範囲を画像縦幅に対する割合で指定\n'
					'    horizontal_flip: 水平方向の反転有無(True or False)')
	parser.add_argument('--optimizer', dest='optimizer', type=str, default='adam', required=False, \
			help='Optimizer(adam(default), sgd, adam_lrs, sgd, lrs)\n'
					'  * lrs: Learning Rate Scheduler')
	parser.add_argument('--batch_size', dest='batch_size', type=int, default=32, required=False, \
			help='ミニバッチサイズ')
	parser.add_argument('--result_dir', dest='result_dir', type=str, default='./result', required=False, \
			help='学習結果の出力先ディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- NumPy配列形状表示 ---
	def print_ndarray_shape(ndarr):
		if (ndarr is not None):
			print(ndarr.shape)
		else:
			pass
		return
		
	# --- 引数処理 ---
	args = ArgParser()
	print('[INFO] Arguments')
	print('  * args.data_type = {}'.format(args.data_type))
	print('  * args.dataset_dir = {}'.format(args.dataset_dir))
	print('  * args.model_type = {}'.format(args.model_type))
	print('  * args.data_augmentation = {}'.format(args.data_augmentation))
	print('  * args.optimizer = {}'.format(args.optimizer))
	print('  * args.batch_size = {}'.format(args.batch_size))
	print('  * args.result_dir = {}'.format(args.result_dir))
	
	# --- Data Augmentationパラメータを辞書型に変換 ---
	if (args.data_augmentation is not None):
		dict_keys = ['rotation_range', 'width_shift_range', 'height_shift_range', 'horizontal_flip']
		df_da_params = pd.read_csv(io.StringIO(args.data_augmentation), header=None, skipinitialspace=True).values[0]
		
		data_augmentation = {}
		for (key, da_param) in zip(dict_keys, df_da_params):
			data_augmentation[key] = da_param
	else:
		data_augmentaion = None
	
	if (args.data_type == "MNIST"):
		dataset = DataLoaderMNIST(args.dataset_dir, validation_split=0.2)
		print_ndarray_shape(dataset.train_images)
		print_ndarray_shape(dataset.train_labels)
		print_ndarray_shape(dataset.validation_images)
		print_ndarray_shape(dataset.validation_labels)
		print_ndarray_shape(dataset.test_images)
		print_ndarray_shape(dataset.test_labels)
		
		if (dataset.train_images is not None):
			x_train = dataset.train_images / 255
		else:
			x_train = None
		y_train = dataset.train_labels
		if (dataset.validation_images is not None):
			x_val = dataset.validation_images / 255
		else:
			x_val = None
		y_val = dataset.validation_labels
		if (dataset.test_images is not None):
			x_test = dataset.test_images / 255
		else:
			x_test = None
		y_test = dataset.test_labels
		output_dims = dataset.output_dims
	elif (args.data_type == "CIFAR-10"):
		dataset = DataLoaderCIFAR10(args.dataset_dir, validation_split=0.2)
		print_ndarray_shape(dataset.train_images)
		print_ndarray_shape(dataset.train_labels)
		print_ndarray_shape(dataset.validation_images)
		print_ndarray_shape(dataset.validation_labels)
		print_ndarray_shape(dataset.test_images)
		print_ndarray_shape(dataset.test_labels)
		
		if (dataset.train_images is not None):
			x_train = dataset.train_images / 255
		else:
			x_train = None
		y_train = dataset.train_labels
		if (dataset.validation_images is not None):
			x_val = dataset.validation_images / 255
		else:
			x_val = None
		y_val = dataset.validation_labels
		if (dataset.test_images is not None):
			x_test = dataset.test_images / 255
		else:
			x_test = None
		y_test = dataset.test_labels
		output_dims = dataset.output_dims
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
	
	if (args.model_type == 'MLP'):
		trainer = TrainerMLP(dataset.train_images.shape[1:], output_dir=args.result_dir, optimizer=args.optimizer)
		trainer.fit(x_train, y_train, x_val=x_val, y_val=y_val, x_test=x_test, y_test=y_test,
			batch_size=args.batch_size, da_params=data_augmentation)
		trainer.save_model()
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	elif (args.model_type == 'SimpleCNN'):
		trainer = TrainerCNN(dataset.train_images.shape[1:], output_dir=args.result_dir, optimizer=args.optimizer)
		trainer.fit(x_train, y_train, x_val=x_val, y_val=y_val, x_test=x_test, y_test=y_test,
			batch_size=args.batch_size, da_params=data_augmentation)
		trainer.save_model()
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	elif (args.model_type == 'SimpleResNet'):
		trainer = TrainerResNet(dataset.train_images.shape[1:], output_dims, output_dir=args.result_dir, optimizer=args.optimizer)
		trainer.fit(x_train, y_train, x_val=x_val, y_val=y_val, x_test=x_test, y_test=y_test,
			batch_size=args.batch_size, da_params=data_augmentation)
		trainer.save_model()
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	else:
		print('[ERROR] Unknown model_type: {}'.format(args.model_type))
		quit()

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

