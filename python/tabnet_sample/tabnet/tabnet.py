#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
import torch

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
		kf = KFold(n_splits=kf_splits, shuffle=False)
		scores = []
		self.tabnet_clf_models = []
		
		for i, (train_index, val_index) in enumerate(kf.split(x_train, y_train)):
			tabnet_params = dict(
								verbose=40,
								optimizer_fn=torch.optim.Adam,
								optimizer_params=dict(lr=1e-2, weight_decay=1e-5),
								scheduler_params=dict(max_lr=0.05, steps_per_epoch=x_train.shape[0] // 128, epochs=300),
								scheduler_fn=torch.optim.lr_scheduler.OneCycleLR)
			tabnet_clf = TabNetClassifier(**tabnet_params)
			
			x_tr = x_train[train_index]
			x_val = x_train[val_index]
			y_tr = y_train[train_index]
			y_val = y_train[val_index]
			
			tabnet_clf.fit(
				x_tr, y_tr,
				eval_set=[(x_val, y_val)],
				eval_metric=['accuracy'],
				patience=100,
				max_epochs=500
			)
			self.tabnet_clf_models.append(tabnet_clf)
			prediction = tabnet_clf.predict(x_val)
			scores.append(accuracy_score(y_val, prediction))
			
			if (i == 0):
				feature_importances = tabnet_clf.feature_importances_.copy()
			else:
				feature_importances = np.vstack((feature_importances, tabnet_clf.feature_importances_))
		
		print(scores)
		print(np.mean(scores))
		
		return scores, feature_importances
	
	def inference(self, x_test):
		for i, tabnet_clf in enumerate(self.tabnet_clf_models):
			if (i == 0):
				prediction = tabnet_clf.predict(x_test)
			else:
				prediction = np.vstack((prediction, tabnet_clf.predict(x_test)))
		
		return prediction

