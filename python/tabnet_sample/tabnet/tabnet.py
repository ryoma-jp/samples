#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------

#---------------------------------
# クラス
#---------------------------------
class TabNet():
	def __init__(self):
		return
	
	def fit(self, x_train, y_train, kf_splits=5):
		tabnet_params = dict(verbose=40)
		tabnet_clf = TabNetClassifier(**tabnet_params)
		kf = KFold(n_splits=kf_splits, shuffle=False)
		scores = []
		
		for train_index, val_index in kf.split(x_train, y_train):
			x_tr = x_train[train_index]
			x_val = x_train[val_index]
			y_tr = y_train[train_index]
			y_val = y_train[val_index]
			
			tabnet_clf.fit(
				x_tr, y_tr,
				eval_set=[(x_val, y_val)],
				patience=100,
				max_epochs=300
			)
			prediction = tabnet_clf.predict(x_val)
			scores.append(accuracy_score(y_val, prediction))
		
		print(scores)
		print(np.mean(scores))
		
		return


