#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

#---------------------------------
# 定数定義
#---------------------------------
identity = np.eye(10, dtype=np.int)

#---------------------------------
# 関数
#---------------------------------
def unpickle(file):
	import pickle
	with open(file, 'rb') as fo:
		dict = pickle.load(fo, encoding='bytes')
	return dict

def load_cifar10(dataset_dir):
	# --- load training data ---
	train_data_list = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5"]
	dict_data = unpickle(os.path.join(dataset_dir, train_data_list[0]))
	train_images = dict_data[b'data']
	train_labels = [identity[i] for i in dict_data[b'labels']]
	for train_data in train_data_list[1:]:
		dict_data = unpickle(os.path.join(dataset_dir, train_data))
		train_images = np.vstack((train_images, dict_data[b'data']))
		train_labels = np.vstack((train_labels, [identity[i] for i in dict_data[b'labels']]))
	
	# --- load test data ---
	test_data = "test_batch"
	dict_data = unpickle(os.path.join(dataset_dir, test_data))
	test_images = dict_data[b'data']
	test_labels = [identity[i] for i in dict_data[b'labels']]
	
	# --- transpose: [N, C, H, W] -> [N, H, W, C] ---
	train_images = train_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
	test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
	
	return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



