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
import cv2

#---------------------------------
# 定数定義
#---------------------------------
# --- 数値判定用正規表現 ---
numbers = re.compile(r'(\d+)')

#---------------------------------
# 関数
#---------------------------------
def load_movie_poster(dataset_dir, output_dir='./output'):
	def _numericalSort(value):
		parts = numbers.split(value)
		parts[1::2] = map(int, parts[1::2])
		return parts
	
	def _extract_classification_info(list_ground_truth, img_dir):
		keys = ['{', '}', '"imdbID"', '"Poster"', '"Genre"']
		
		anns = []
		for i, ground_truth in enumerate(list_ground_truth):
			# --- metaファイル読み込み ---
			#   * 文字コードが混在している為，テキストを開く際に文字コード指定する
			print('[INFO] load {} ({}/{})'.format(ground_truth, i, len(list_ground_truth)))
			with open(ground_truth, 'rb') as f:
				enc = detect(f.read())
			with open(ground_truth, 'r', encoding=enc['encoding']) as f:
				lines = f.readlines()
			
			# --- metaファイルから画像ファイル情報と分類クラス情報を読み込む ---
			for i, line in enumerate(lines):
				for key in keys:
					if (key in line):
						if (key == '{'):
							str_anns = ""
							line_prev = line
						elif (key == '}'):
							str_anns += '"Year": {},\n'.format(os.path.splitext(os.path.basename(ground_truth))[0])
							str_anns += line_prev.replace(',\n', '\n')
							str_anns += line
							ann = json.loads(str_anns)
							img_file = os.path.join(img_dir, str(ann['Year']), '{}.jpg'.format(ann['imdbID']))
							if (os.path.exists(img_file)):
								anns.append(ann)
						else:
							str_anns += line_prev
							line_prev = line
						break
			
		return anns
	
	os.makedirs(output_dir, exist_ok=True)
	img_dir = os.path.join(dataset_dir, "Movie_Poster_Dataset")
	meta_dir = os.path.join(dataset_dir, "groundtruth")
	
	# --- Grand-Truthのファイル群を取得 ---
	list_ground_truth = sorted(glob.glob(os.path.join(meta_dir, '*.txt')), key=_numericalSort)
	print(list_ground_truth)
	
	# --- データ読み込み ---
	anns = _extract_classification_info(list_ground_truth, img_dir)
#	print(anns)
	print('[INFO] Meta data loaded')
	print('  * Num of annotations: {}'.format(len(anns)))
	print('  * Num of classification keys: {}'.format(anns[0].keys()))
	
	img_size = []
	log_interval = len(anns) // 30
	for i, ann in enumerate(anns):
		if (i % log_interval == 0):
			print('[INFO] Processing ... ({}/{})'.format(i, len(anns)))
		img_file = os.path.join(img_dir, str(ann['Year']), '{}.jpg'.format(ann['imdbID']))
		img = cv2.imread(img_file)
		if (img is not None):
			ann['imgHeight'], ann['imgWidth'] = img.shape[0:2]
			img_size.append(img.shape[0:2])
		else:
			print('[ERROR] Failed to open file: {}'.format(img_file))
			quit()
	img_size = np.array(img_size)
	print('[INFO] DONE ({}/{})'.format(len(anns), len(anns)))
	print('  * img_min(h, w): {}'.format(img_size.min(axis=0)))
	print('  * img_max(h, w): {}'.format(img_size.max(axis=0)))
	
	with open(os.path.join(output_dir, 'annotations.json'), mode='w', encoding='utf-8') as f:
		json.dump(anns, f, ensure_ascii=False, indent=2)
	
	quit()
	
	return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)



