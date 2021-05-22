#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
from pycocotools.coco import COCO

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#  * ann_type: ロードするアノテーションの種類('captions', 'instances' or 'person_keypoints')
#---------------------------------
def load_coco2014(dataset_dir, ann_type='instances'):
	# --- directories ---
	ann_dir = os.path.join(dataset_dir, 'annotations')
	train_dir = os.path.join(dataset_dir, 'train2014')
	test_dir = os.path.join(dataset_dir, 'test2014')
	val_dir = os.path.join(dataset_dir, 'val2014')
	
	# --- load data ---
	coco = COCO(os.path.join(ann_dir, '{}_train2014.json'.format(ann_type)))
	annIds = coco.getAnnIds()
	train_labels = coco.loadAnns(annIds)
	print('[INFO] Total annotations: {}'.format(len(train_labels)))
	
	imgIds = coco.getImgIds()
	train_images = coco.loadImgs(imgIds)
	print('[INFO] Total images: {}'.format(len(train_images)))
	
	if (ann_type == 'captions'):
		pass
	elif (ann_type == 'instances'):
		catIds = coco.getCatIds()
		cats = coco.loadCats(catIds)
		print('[INFO] Num of categories: {}'.format(len(cats)))
		names = [cat['name'] for cat in cats]
		print('[INFO] COCO categories: \n{}\n'.format(' '.join(names)))
	elif (ann_type == 'person_keypoints'):
		pass
	else:
		print('[ERROR] undefined ann_tyep: {}'.format(ann_type))
		quit()
	
	# --- load data ---
	print('[T.B.D] store dummy data')
	train_images = [0, 1]
	train_labels = [0, 1]
	validation_images = [0, 1]
	validation_labels = [0, 1]
	test_images = [0, 1]
	test_labels = [0, 1]
	
	return np.array(train_images), train_labels, \
			np.array(validation_images), validation_labels, \
			np.array(test_images)



