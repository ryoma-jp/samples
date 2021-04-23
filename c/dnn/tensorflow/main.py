# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd
from dataloader import *
from tf_model import *

def ArgParser():
	parser = argparse.ArgumentParser(description='TensorFlowでのCNN学習',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットのディレクトリ')
	parser.add_argument('--model_dir', dest='model_dir', type=str, default='./output', required=True, \
			help='学習済みモデルを保存するディレクトリ')

	args = parser.parse_args()

	return args


def main():
	input_dims = [None, 32, 32, 3]
	conv_channels = [32, 64, 128]
	conv_kernel_size = [3, 3, 3]
	pool_size = [2, 2]
	fc_channels = [128]
	output_dims = [None, 10]
	dropout_rate = 0.5

	args = ArgParser()
	os.makedirs(args.model_dir, exist_ok=True)
	
	dataset = DataLoader(data_type=DataLoader.TYPE_CIFAR10, data_dir=args.dataset_dir, validation_ratio=0.1)
	print(dataset.train_data.shape)
	print(dataset.train_label.shape)
	print(dataset.test_data.shape)
	print(dataset.test_label.shape)

	tf_model = TF_Model()
	train_x, train_y, train_y_ = tf_model.conv_net(
									input_dims,
									conv_channels,
									conv_kernel_size,
									pool_size,
									fc_channels,
									output_dims,
									dropout_rate,
									True)
	test_x, test_y, test_y_ = tf_model.conv_net(
									input_dims,
									conv_channels,
									conv_kernel_size,
									pool_size,
									fc_channels,
									output_dims,
									dropout_rate,
									False)

	n_epoch = 200
	n_minibatch = 64
	optimizer = 'Adam'
	learning_rate = 0.0001
	weight_decay = 0.001

	train_acc, test_acc = tf_model.fit(
							dataset,
							train_x, train_y, train_y_,
							test_x, test_y, test_y_,
							n_epoch, n_minibatch, optimizer, learning_rate, weight_decay,
							args.model_dir)

	print(train_acc, test_acc)

	return

if __name__=='__main__':
	main()


