#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse

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
	parser.add_argument('--result_dir', dest='result_dir', type=str, default='./result', required=False, \
			help='学習結果の出力先ディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print('[INFO] Arguments')
	print('  * args.data_type = {}'.format(args.data_type))
	print('  * args.dataset_dir = {}'.format(args.dataset_dir))
	print('  * args.model_type = {}'.format(args.model_type))
	print('  * args.result_dir = {}'.format(args.result_dir))
	
	if (args.data_type == "MNIST"):
		dataset = DataLoaderMNIST(args.dataset_dir)
		print(dataset.train_images.shape)
		print(dataset.train_labels.shape)
		print(dataset.test_images.shape)
		print(dataset.test_labels.shape)
		
		x_train = dataset.train_images / 255
		y_train = dataset.train_labels
		x_test = dataset.test_images / 255
		y_test = dataset.test_labels
		output_dims = dataset.output_dims
	elif (args.data_type == "CIFAR-10"):
		dataset = DataLoaderCIFAR10(args.dataset_dir)
		print(dataset.train_images.shape)
		print(dataset.train_labels.shape)
		print(dataset.test_images.shape)
		print(dataset.test_labels.shape)
		
		x_train = dataset.train_images / 255
		y_train = dataset.train_labels
		x_test = dataset.test_images / 255
		y_test = dataset.test_labels
		output_dims = dataset.output_dims
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
	
	if (args.model_type == 'MLP'):
		trainer = TrainerMLP(dataset.train_images.shape[1:], output_dir=args.result_dir)
		trainer.fit(x_train, y_train, x_test=x_test, y_test=y_test)
		trainer.save_model()
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	elif (args.model_type == 'SimpleCNN'):
		trainer = TrainerCNN(dataset.train_images.shape[1:], output_dir=args.result_dir)
		trainer.fit(x_train, y_train, x_test=x_test, y_test=y_test)
		trainer.save_model()
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	elif (args.model_type == 'SimpleResNet'):
		trainer = TrainerResNet(dataset.train_images.shape[1:], output_dims, output_dir=args.result_dir)
		trainer.fit(x_train, y_train, x_test=x_test, y_test=y_test)
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

