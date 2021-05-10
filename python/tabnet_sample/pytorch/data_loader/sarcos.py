#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
from scipy.io import loadmat

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def load_sarcos(dataset_dir):
	# --- load sarcos_inv.mat ---
	train_data = loadmat(os.path.join(dataset_dir, 'sarcos_inv.mat'))
	
	# --- sarcos_inv_test.mat ---
	test_data = loadmat(os.path.join(dataset_dir, 'sarcos_inv_test.mat'))
	
	return train_data['sarcos_inv'][:, 0:21], train_data['sarcos_inv'][:, 21:28], \
			test_data['sarcos_inv_test'][:, 0:21], test_data['sarcos_inv_test'][:, 21:28]



