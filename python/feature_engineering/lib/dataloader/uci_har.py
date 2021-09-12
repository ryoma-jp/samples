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
	
	# --- 特徴量名を取得 ---
	feature_name_file = os.path.join(dataset_dir, 'features.txt')
	df_feature_name = pd.read_csv(feature_name_file, sep='\s+', header=None)
	feature_name = df_feature_name.values[:, 1]
	
	
	# --- ラベル名を取得 ---
	activity_name_file = os.path.join(dataset_dir, 'activity_labels.txt')
	df_activity_name = pd.read_csv(activity_name_file, sep='\s+', header=None)
	activity_name = {}
	for _activity_name in df_activity_name.values:
		activity_name[_activity_name[0]] = _activity_name[1]
	
	return x_train.values, y_train.values, x_test.values, y_test.values, feature_name, activity_name



