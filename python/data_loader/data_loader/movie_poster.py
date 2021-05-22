#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import re
import glob
import json
import numpy as np
from chardet import detect

#---------------------------------
# 定数定義
#---------------------------------
# --- 数値判定用正規表現 ---
numbers = re.compile(r'(\d+)')

#---------------------------------
# 関数
#---------------------------------
def load_movie_poster(dataset_dir):
	def _numericalSort(value):
		parts = numbers.split(value)
		parts[1::2] = map(int, parts[1::2])
		return parts
	
	def _extract_classification_info(list_ground_truth):
		keys = ['{', '}', '"imdbID"', '"Poster"', '"Genre"']
		
		anns = []
		for ground_truth in list_ground_truth:
			print('[INFO] load {}'.format(ground_truth))
			print('  * 文字コードが混在している為，テキストを開く際に文字コード指定する')
			with open(ground_truth, 'rb') as f:
				enc = detect(f.read())
			with open(ground_truth, 'r', encoding=enc['encoding']) as f:
				lines = f.readlines()
			
			for i, line in enumerate(lines):
				for key in keys:
					if (key in line):
						if (key == '{'):
							str_anns = ""
							line_prev = line
						elif (key == '}'):
							str_anns += line_prev.replace(',\n', '\n')
							str_anns += line
							anns.append(json.loads(str_anns))
						else:
							str_anns += line_prev
							line_prev = line
						break
			
		return anns
	
	img_dir = os.path.join(dataset_dir, "Movie_Poster_Dataset")
	meta_dir = os.path.join(dataset_dir, "groundtruth")
	
	# --- Grand-Truthのファイル群を取得 ---
	list_ground_truth = sorted(glob.glob(os.path.join(meta_dir, '*.txt')), key=_numericalSort)
	print(list_ground_truth)
	
	# --- データ読み込み ---
	anns = _extract_classification_info(list_ground_truth)
	print(anns)
	print(len(anns))
	quit()
	
	return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



