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
		"""
			https://canvas.harvard.edu/files/260014/download?download_frd=1&verifier=law8QK56wDa47yRCbBnVH0akY4Q8aqDMWgsclJJV
			 * Algorithm 4 K-Medoids
		"""
		if (len(data.shape) > 2):
			# --- 二次元[N, d]にreshape ---
			data = np.reshape(data, [len(data), -1])
		
		print(data.shape)
		
		# --- 各データサンプルのクラスタを乱数で初期設定 ---
		r = np.random.choice(range(self.n_cluster), len(data))
		
		# --- 入力データのサンプル間距離行列を生成 ---
		D = squareform(pdist(data, metric='euclidean'))
		
		# --- クラスタリング実行 ---
		mu = np.zeros(self.n_cluster, dtype=int)	# セントロイド
		for _iter in range(self.max_iter):
			for k in range(self.n_cluster):
				index = np.where(r==k)[0]
				J = D[index][:, index].sum(axis=1)
				mu[k] = index[np.argmin(J)]
				print('[INFO] iter={}, k={}, n_samples: {}'.format(_iter, k, len(index)))
			
			r_prev = r.copy()
			r = np.argmin(D[:, mu], axis=1)

			if (np.all(r_prev == r)):
				break
			
		return r, mu
	
	def predict(self):
		return

