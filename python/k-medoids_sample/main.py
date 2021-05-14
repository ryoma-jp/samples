#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
import cv2
import numpy as np
from data_loader import cifar10
from kmedoids import kmedoids
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='k-medoids法によるクラスタリングのサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--data_type', dest='data_type', type=str, default='CIFAR-10', required=False, \
			help='データ種別(CIFAR-10, BLOBS, or ...(T.B.D)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=True, \
			help='データセットディレクトリ')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default='./output', required=True, \
			help='出力ディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.data_type)
	print(args.dataset_dir)
	print(args.output_dir)
	
	os.makedirs(args.output_dir, exist_ok=True)
	
	if (args.data_type == "CIFAR-10"):
		train_data, train_labels, test_data, test_labels = cifar10.load_cifar10(args.dataset_dir)
		#data = train_data
		data = train_data[0:10000]
		n_cluster = 10
	elif (args.data_type == "BLOBS"):
		n_cluster = 3
		data, labels = make_blobs(
										n_samples=150,
										n_features=2,
										centers=n_cluster,
										cluster_std=1.5,
										shuffle=True,
										random_state=0)
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
		
	
	km = kmedoids.kMedoids(n_cluster=n_cluster, result_dir=args.output_dir)
#	km.fit(train_data)		# メモリ不足エラー(16GB以上必要)
#	km.fit(test_data[0:100])			# for Debug
	labels, medoids = km.fit(data)
	
	if (data.shape[1] == 2):
		plt.figure()
		for i, label in enumerate(sorted(np.unique(labels))):
			plt.scatter(
				data[labels==label, 0],
				data[labels==label, 1])
		plt.scatter(data[medoids, 0], data[medoids, 1], c='red')
		plt.tight_layout()
		plt.savefig(os.path.join(args.output_dir, 'k-medoids.png'))
	
	if (args.data_type == "CIFAR-10"):
		# --- Medoidの画像を保存 ---
		for i in range(len(medoids)):
			(h, w, c) = data[0].shape
			n = int(np.ceil(np.sqrt(len(medoids))))
			
			img = np.zeros([h*n, w*n, c], dtype=np.uint8)
			cnt = 0
			for nh in range(n):
				for nw in range(n):
					img[h*nh:h*(nh+1), w*nw:w*(nw+1)] = data[medoids[cnt]]
					cnt += 1
					if (cnt >= len(medoids)):
						break
				if (cnt >= len(medoids)):
					break
			cv2.imwrite(os.path.join(args.output_dir, 'img_medoids.png'), img)
			
		# --- クラスタ毎の画像を保存 ---
		for i in range(len(medoids)):
			(h, w, c) = data[0].shape
			
			n = 4
			img = np.zeros([h*n, w*n, c], dtype=np.uint8)
			cluster_img = data[labels==i]
			
			cnt = 0
			for nh in range(n):
				for nw in range(n):
					img[h*nh:h*(nh+1), w*nw:w*(nw+1)] = cluster_img[cnt]
					cnt += 1
					if (cnt >= len(cluster_img)):
						break
				if (cnt >= len(cluster_img)):
					break
			cv2.imwrite(os.path.join(args.output_dir, 'img_cluster{}.png'.format(i)), img)
			
	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

