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
def load_mnist(dataset_dir, flatten=True, one_hot=True):
	# --- load training data ---
	f = open(os.path.join(dataset_dir, 'train-images-idx3-ubyte'))
	byte_data = np.fromfile(f, dtype=np.uint8)
	
	n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
	img_h = (byte_data[8] << 24) | (byte_data[9] << 16) | (byte_data[10] << 8) | (byte_data[11])
	img_w = (byte_data[12] << 24) | (byte_data[13] << 16) | (byte_data[14] << 8) | (byte_data[15])
	
	if (flatten):
		train_images = byte_data[16:].reshape(n_items, -1)
	else:
		train_images = byte_data[16:].reshape(n_items, img_h, img_w)
	
	# --- load training label ---
	f = open(os.path.join(dataset_dir, 'train-labels-idx1-ubyte'))
	byte_data = np.fromfile(f, dtype=np.uint8)
	
	n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
	
	train_labels = byte_data[8:]
	if (one_hot):
		train_labels = np.array([identity[i] for i in train_labels])
	
	# --- load test data ---
	f = open(os.path.join(dataset_dir, 't10k-images-idx3-ubyte'))
	byte_data = np.fromfile(f, dtype=np.uint8)
	
	n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
	img_h = (byte_data[8] << 24) | (byte_data[9] << 16) | (byte_data[10] << 8) | (byte_data[11])
	img_w = (byte_data[12] << 24) | (byte_data[13] << 16) | (byte_data[14] << 8) | (byte_data[15])
	
	if (flatten):
		test_images = byte_data[16:].reshape(n_items, -1)
	else:
		test_images = byte_data[16:].reshape(n_items, img_h, img_w)
	
	# --- load test label ---
	f = open(os.path.join(dataset_dir, 't10k-labels-idx1-ubyte'))
	byte_data = np.fromfile(f, dtype=np.uint8)
	
	n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
	
	test_labels = byte_data[8:]
	if (one_hot):
		test_labels = np.array([identity[i] for i in test_labels])
	
	return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



