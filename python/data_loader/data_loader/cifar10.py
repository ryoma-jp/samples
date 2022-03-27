#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import cv2
import tqdm
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

def load_cifar10(dataset_dir, img_dir=None):
	# --- load training data ---
	train_data_list = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5"]
	dict_data = unpickle(os.path.join(dataset_dir, train_data_list[0]))
	train_images = dict_data[b'data']
	train_labels = [identity[i] for i in dict_data[b'labels']]
	train_filenames = dict_data[b'filenames']
	for train_data in tqdm.tqdm(train_data_list[1:]):
		dict_data = unpickle(os.path.join(dataset_dir, train_data))
		train_images = np.vstack((train_images, dict_data[b'data']))
		train_labels = np.vstack((train_labels, [identity[i] for i in dict_data[b'labels']]))
		train_filenames = np.hstack((train_filenames, dict_data[b'filenames']))
	
	# --- load test data ---
	test_data = "test_batch"
	dict_data = unpickle(os.path.join(dataset_dir, test_data))
	test_images = dict_data[b'data']
	test_labels = [identity[i] for i in dict_data[b'labels']]
	test_filenames = dict_data[b'filenames']
	
	# --- transpose: [N, C, H, W] -> [N, H, W, C] ---
	train_images = train_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
	test_images = test_images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)

	# --- save image data ---
	#  * if img_dir is not None
	if (img_dir is not None):
		# --- create output directories ---
		os.makedirs(os.path.join(img_dir, 'train'), exist_ok=True)
		os.makedirs(os.path.join(img_dir, 'test'), exist_ok=True)

		# --- train images ---
		for (img, filename) in tqdm.tqdm(zip(train_images, train_filenames), total=len(train_images)):
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
			cv2.imwrite(os.path.join(img_dir, 'train', filename.decode()), img)

		# --- test images ---
		for (img, filename) in tqdm.tqdm(zip(test_images, test_filenames), total=len(test_images)):
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
			cv2.imwrite(os.path.join(img_dir, 'test', filename.decode()), img)
	
	return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



