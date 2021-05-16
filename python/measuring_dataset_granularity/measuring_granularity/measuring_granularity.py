#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import cv2
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
			class_idx = np.arange(len(label))[label==i]
			data_tmp = data[class_idx]
			print('i: {}, len(data_tmp): {}'.format(i, len(data_tmp)))
			
			# --- クラスiのサンプル間距離行列を生成 ---
			D = squareform(pdist(data_tmp, metric='euclidean'))
			
			# --- サンプル間距離の合計が最も小さいサンプルがmedoid ---
			medoid.append(class_idx[np.argmax(D.sum(axis=0))])
			
		return medoid
	
	def rsm(self, data, label, data_type=DATA_TYPE_IMAGE, onehot=False, output_dir='./output'):
		# --- 準備 ---
		rsm_output_dir = os.path.join(output_dir, 'rsm')
		os.makedirs(rsm_output_dir, exist_ok=True)
		if (onehot):
			label = np.argmax(label, axis=1)
			print(label[0])
		if (len(data.shape) > 2):
			data_calc = np.reshape(data, [len(data), -1])
		else:
			data_calc = data
		
		# --- medoid取得 ---
		medoids = self._get_medoid(data, label)
		print(medoids)
		if (data_type == self.DATA_TYPE_IMAGE):
			for i, idx in enumerate(medoids):
				img = data[idx]
				cv2.imwrite(os.path.join(rsm_output_dir, 'img_medoid_{}.png'.format(i)), img)
		
		# --- ground-truthクラスとの距離計算 ---
		n_class = max(label)+1
		for i in range(n_class):
			# --- クラスiのデータを取得 ---
			data_tmp = data_calc[np.arange(len(label))[label==i]]
			print('i: {}, len(data_tmp): {}'.format(i, len(data_tmp)))
			
			data_tmp_dist = np.sqrt(np.sum((data_tmp - data_calc[medoids[i]])**2, axis=1))
			print(data_tmp_dist)
			print(data_tmp_dist.shape)
			if (i == 0):
				data_dist = data_tmp_dist
			else:
				data_dist = np.vstack((data_dist, data_tmp_dist))
		print(data_dist.shape)
		
		# --- 他クラスのmedoidとの距離計算 ---
		data_medoids = data_calc[medoids]
		print(data_medoids)
		for i, data_medoid in enumerate(data_medoids):
			data_tmp_dist_other_medoid = np.sqrt(np.sum((data_calc - data_medoid)**2, axis=1))
			print(data_tmp_dist_other_medoid.shape)
			if (i == 0):
				data_dist_other_medoid = data_tmp_dist_other_medoid
			else:
				data_dist_other_medoid = np.vstack((data_dist_other_medoid, data_tmp_dist_other_medoid))
		print(data_dist_other_medoid.shape)
#		print(data_dist_other_medoid[:, 0])
#		print(data_dist_other_medoid[6, 0])
		print(data_dist_other_medoid[:, medoids])
		
		# --- ラベルとmedoidとの距離の小さいインデックスを保存 ---
		data_dist_other_medoid_argmin = np.argmin(data_dist_other_medoid, axis=0)
		data_dist_other_medoid_min = np.min(data_dist_other_medoid, axis=0)
		pd.DataFrame(np.vstack((label, data_dist_other_medoid_argmin, data_dist_other_medoid_min)).T).to_csv(os.path.join(rsm_output_dir, 'label_vs_medoid_idx.csv'), header=False, index=False)
		
		return 
	
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



