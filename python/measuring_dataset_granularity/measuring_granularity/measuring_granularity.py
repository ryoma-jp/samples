#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import cv2
import numpy as np
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
class MeasuringGranularity():
	# --- DATA_TYPE ---
	DATA_TYPE_IMAGE = 'image'
	
	def __init__(self):
		return
	
	def _get_medoid(self, data, label, onehot=False):
		if (len(data.shape) > 2):
			# --- 二次元[N, d]にreshape ---
			data = np.reshape(data, [len(data), -1])
		
		# --- クラスラベルごとにmedoidを算出 ---
		if (onehot):
			label = np.argmax(label, axis=1)
		n_class = max(label)+1
		medoid = []
		print('n_class: {}'.format(n_class))
		for i in range(n_class):
			# --- クラスiのデータを取得 ---
			data_tmp = data[np.arange(len(label))[label==i]]
			print('i: {}, len(data_tmp): {}'.format(i, len(data_tmp)))
			
			# --- クラスiのサンプル間距離行列を生成 ---
			D = squareform(pdist(data_tmp, metric='euclidean'))
			
			# --- サンプル間距離の合計が最も小さいサンプルがmedoid ---
			medoid.append(np.argmax(D.sum(axis=0)))
			
		return medoid
	
	def rankm(self, data, label, data_type=DATA_TYPE_IMAGE, onehot=False, output_dir='./output'):
		# --- 準備 ---
		rankm_output_dir = os.path.join(output_dir, 'rankm')
		os.makedirs(rankm_output_dir, exist_ok=True)
		if (onehot):
			label = np.argmax(label, axis=1)
		
		# --- medoid取得 ---
		medoids = self._get_medoid(data, label)
		print(medoids)
		if (data_type == self.DATA_TYPE_IMAGE):
			for i, idx in enumerate(medoids):
				img = data[idx]
				cv2.imwrite(os.path.join(rankm_output_dir, 'img_medoid_{}.png'.format(i)), img)
		
		return 



