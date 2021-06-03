#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import argparse
import numpy as np
from data_loader import movie_poster
from classifier import classifier

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def ArgParser():
	parser = argparse.ArgumentParser(description='データセット読み込み処理のサンプル',
				formatter_class=argparse.RawTextHelpFormatter)

	# --- 引数を追加 ---
	parser.add_argument('--data_type', dest='data_type', type=str, default='MoviePoster', required=False, \
			help='データ種別(MoviePoster or ...(T.B.D)')
	parser.add_argument('--dataset_dir', dest='dataset_dir', type=str, default=None, required=False, \
			help='データセットディレクトリ')
	parser.add_argument('--dataset_file', dest='dataset_file', type=str, default=None, required=False, \
			help='データセットファイル')
	parser.add_argument('--output_dir', dest='output_dir', type=str, default='./output', required=False, \
			help='出力先ディレクトリ')

	args = parser.parse_args()

	return args

def main():
	# --- 引数処理 ---
	args = ArgParser()
	print(args.data_type)
	print(args.dataset_dir)
	print(args.dataset_file)
	print(args.output_dir)
	
	# --- 出力ディレクトリ作成 ---
	os.makedirs(args.output_dir, exist_ok=True)
	
	# --- データ読み込み ---
	if (args.data_type == "MoviePoster"):
		output_dir = os.path.join(args.output_dir, 'movie_poster')
		train_images, train_labels, test_images, test_labels = movie_poster.load_movie_poster(args.dataset_dir, output_dir=output_dir, random_seed=0, resize=[300, 300])
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
		
		np.savez_compressed(os.path.join(output_dir, 'dataset_movie_poster.npz'), 
			train_images, train_labels, test_images, test_labels)
		
	elif (args.data_type == "MoviePoster_npz"):
		npz_comp = np.load(args.dataset_file)
		train_images = npz_comp['arr_0']
		train_labels = npz_comp['arr_1']
		test_images = npz_comp['arr_2']
		test_labels = npz_comp['arr_3']
		
		print(train_images.shape)
		print(train_labels.shape)
		print(test_images.shape)
		print(test_labels.shape)
	else:
		print('[ERROR] Unknown data_type: {}'.format(args.data_type))
		quit()
	
	classifier.trainer(train_images, train_labels)

	return

#---------------------------------
# メイン処理
#---------------------------------
if __name__ == '__main__':
	main()

