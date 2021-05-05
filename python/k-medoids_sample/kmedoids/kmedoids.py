#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------

#---------------------------------
# クラス
#---------------------------------
class kMedoids():
	def __init__(self, n_cluster, max_iter=300, result_dir='./output'):
		self.n_cluster = n_cluster
		self.max_iter = max_iter
		self.result_dir=result_dir
		os.makedirs(self.result_dir, exist_ok=True)
		return
	
	def fit(self, data):
		if (len(data.shape) > 2):
			# --- 二次元[N, d]にreshape ---
			data = np.reshape(data, [len(data), -1])
		
		print(data.shape)
		
		# --- 初期セントロイドを選択（乱数） ---
		medoids = np.random.choice(range(len(data)), self.n_cluster, replace=False)
		print('[INFO] medoids={}'.format(medoids))
		pdist_data = pdist(data, metric='euclidean')
		print(pdist_data.shape)
		D = squareform(pdist_data)
#		pd.DataFrame(D).to_csv(os.path.join(self.result_dir, 'D.csv'))
		print(D.shape)
		tmp_D = D[:, medoids]
#		print(tmp_D)
		
		labels = np.argmin(tmp_D, axis=1)
		print(labels)
		
		for _iter in range(self.max_iter):
			for i in range(self.n_cluster):
				# --- クラスタのインデックスを取得 ---
				index = np.where(labels==i)[0]
#				print(index)
				
				# --- クラスタのデータを取得 ---
				tmp_D = D[index]
				tmp_D = tmp_D[:, index]
#				print(tmp_D.shape)
				
				# --- クラスタ内の距離合計を算出 ---
				tmp_D_sum = np.sum(tmp_D, axis=1)
#				print(tmp_D_sum.shape)
				
				# --- 合計距離が最小のデータをセントロイドに変更する ---
				medoids[i] = index[np.argmin(tmp_D_sum)]
			
			print('[INFO] {} (iter={})'.format(medoids, _iter))
			tmp_D = D[:, medoids]
			labels = np.argmin(tmp_D, axis=1)
#			print(labels.shape)
		
		return labels, medoids
	
	def predict(self):
		return

