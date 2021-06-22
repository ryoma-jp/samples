#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse

_data_type = os.environ['DATA_TYPE']
if (_data_type == 'MNIST'):
	from data_loader.data_loader import DataLoaderMNIST
elif (_data_type == 'CIFAR-10'):
	from data_loader.data_loader import DataLoaderCIFAR10
else:
	print('[ERROR] Unknown DATA_TYPE({})'.format(_data_type))
	quit()

from trainer.trainer import TrainerMLP, TrainerCNN

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='TensorFlowの学習実装サンプル\n'
													'  * No.01: MNISTデータセットを用いた全結合NN学習サンプル\n'
													'  * No.02: CIFAR-10データセットを用いたCNN学習サンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--data_type', dest='data_type', type=str, default='CIFAR-10', required=False, \
			help='データ種別(MNIST, CIFAR-10)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.data_type)
	print(args.dataset_dir)
	
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
		trainer = TrainerMLP(dataset.train_images.shape[1:])
		trainer.fit(x_train, y_train, x_test=x_test, y_test=y_test)
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
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
		trainer = TrainerCNN(dataset.train_images.shape[1:])
		trainer.fit(x_train, y_train, x_test=x_test, y_test=y_test)
		
		predictions = trainer.predict(x_test)
		print('\nPredictions(shape): {}'.format(predictions.shape))
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
	

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

