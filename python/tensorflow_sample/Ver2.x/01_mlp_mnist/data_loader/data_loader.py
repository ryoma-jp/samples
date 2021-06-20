#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

#---------------------------------
# クラス; データ取得基底クラス
#---------------------------------
class DataLoader():
	# --- コンストラクタ ---
	def __init__(self):
		return
	
	# --- ラベルインデックス取得 ---
	def get_label_index(self, label, onehot=True):
		if (onehot):
			label = np.argmax(label, axis=1)
		n_category = max(label)+1
		
		return np.array([np.arange(len(label))[label==i] for i in range(n_category)])

#---------------------------------
# クラス; MNISTデータセット取得
#---------------------------------
class DataLoaderMNIST(DataLoader):
	# --- コンストラクタ ---
	def __init__(self, dataset_dir, flatten=False, one_hot=False):
		# --- initialize super class ---
		super().__init__()
		
		# --- load training data ---
		f = open(os.path.join(dataset_dir, 'train-images-idx3-ubyte'))
		byte_data = np.fromfile(f, dtype=np.uint8)
		
		n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
		img_h = (byte_data[8] << 24) | (byte_data[9] << 16) | (byte_data[10] << 8) | (byte_data[11])
		img_w = (byte_data[12] << 24) | (byte_data[13] << 16) | (byte_data[14] << 8) | (byte_data[15])
		
		if (flatten):
			self.train_images = byte_data[16:].reshape(n_items, -1)
		else:
			self.train_images = byte_data[16:].reshape(n_items, img_h, img_w)
		
		# --- load training label ---
		f = open(os.path.join(dataset_dir, 'train-labels-idx1-ubyte'))
		byte_data = np.fromfile(f, dtype=np.uint8)
		
		n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
		
		self.train_labels = byte_data[8:]
		if (one_hot):
			identity = np.eye(10, dtype=np.int)
			self.train_labels = np.array([identity[i] for i in self.train_labels])
		
		# --- load test data ---
		f = open(os.path.join(dataset_dir, 't10k-images-idx3-ubyte'))
		byte_data = np.fromfile(f, dtype=np.uint8)
		
		n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
		img_h = (byte_data[8] << 24) | (byte_data[9] << 16) | (byte_data[10] << 8) | (byte_data[11])
		img_w = (byte_data[12] << 24) | (byte_data[13] << 16) | (byte_data[14] << 8) | (byte_data[15])
		
		if (flatten):
			self.test_images = byte_data[16:].reshape(n_items, -1)
		else:
			self.test_images = byte_data[16:].reshape(n_items, img_h, img_w)
		
		# --- load test label ---
		f = open(os.path.join(dataset_dir, 't10k-labels-idx1-ubyte'))
		byte_data = np.fromfile(f, dtype=np.uint8)
		
		n_items = (byte_data[4] << 24) | (byte_data[5] << 16) | (byte_data[6] << 8) | (byte_data[7])
		
		self.test_labels = byte_data[8:]
		if (one_hot):
			self.test_labels = np.array([identity[i] for i in self.test_labels])
		
		return
	
