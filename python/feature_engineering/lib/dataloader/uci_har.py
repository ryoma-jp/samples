#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import pandas as pd

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def load_uci_har(dataset_dir):
	# --- 学習データ取得 ---
	x_train_file = os.path.join(dataset_dir, 'train', 'X_train.txt')
	y_train_file = os.path.join(dataset_dir, 'train', 'y_train.txt')
	x_train = pd.read_csv(x_train_file, sep='\s+', header=None)
	y_train = pd.read_csv(y_train_file, sep='\s+', header=None)
	
	# --- テストデータ取得 ---
	x_test_file = os.path.join(dataset_dir, 'test', 'X_test.txt')
	y_test_file = os.path.join(dataset_dir, 'test', 'y_test.txt')
	x_test = pd.read_csv(x_test_file, sep='\s+', header=None)
	y_test = pd.read_csv(y_test_file, sep='\s+', header=None)
	
	return x_train, y_train, x_test, y_test



