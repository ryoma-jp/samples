#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def load_flood_modeling(train_ts, test_ts):
	def _parse_ts(ts_file):
		with open(ts_file) as f:
			x = []
			y = []
			for line in f.read().splitlines():
				if (line.startswith('#')):
					# --- SKIP ---
					pass
				elif (line.startswith('@')):
					# --- SKIP ---
					pass
				else:
					_s = line.split(':')
					x.append(_s[0].split(','))
					y.append(_s[1])
		
		return np.array(x, dtype=float), np.array(y, dtype=float)
				
	# --- 学習データ取得 ---
	x_train, y_train = _parse_ts(train_ts)
	
	# --- テストデータ取得 ---
	x_test, y_test = _parse_ts(test_ts)
	
	return x_train, y_train, x_test, y_test



