#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np
import torch

from pytorch_tabnet.pretraining import TabNetPretrainer
from pytorch_tabnet.tab_model import TabNetClassifier, TabNetRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
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
	
	def fit(self, x_train, y_train, kf_splits=5, tabnet_type=None):
		def _get_tabnet_params(tabnet_type):
			if (tabnet_type is None):
				tabnet_params = dict(
									verbose=40,
									optimizer_fn=torch.optim.Adam,
									optimizer_params=dict(lr=1e-2, weight_decay=1e-5),
									scheduler_params=dict(max_lr=0.05, steps_per_epoch=x_train.shape[0] // 128, epochs=300),
									scheduler_fn=torch.optim.lr_scheduler.OneCycleLR)
				fit_params = dict(
									batch_size=1024, virtual_batch_size=128,
									eval_metric='accuracy')
			elif (tabnet_type == 'TabNet-S'):
				tabnet_params = dict(
									n_d=8, n_a=8,
									lambda_sparse=0.0001,
									momentum=0.1,
									n_steps=3,
									gamma=1.2,
									verbose=40,
									optimizer_fn=torch.optim.Adam,
									optimizer_params=dict(lr=0.01),
									scheduler_params=dict(step_size=8000, gamma=0.05),
									scheduler_fn=torch.optim.lr_scheduler.StepLR)
				fit_params = dict(
									batch_size=4096, virtual_batch_size=256,
									eval_metric='mse')
			else:
				print('[ERROR] Unknown tabnet_type: {}'.format(tabnet_type))
				quit()
			
			# --- check problem ---
			if fit_params['eval_metric'] in ['auc', 'accuracy', 'balanced_accuracy', 'logloss']:
				problem = 'classification'
			elif fit_params['eval_metric'] in ['mse', 'mae', 'rmse', 'rmsle']:
				problem = 'regression'
			
			return tabnet_params, fit_params, problem
		
		kf = KFold(n_splits=kf_splits, shuffle=False)
		scores = []
		self.tabnet_models = []
		
		tabnet_params, fit_params, problem = _get_tabnet_params(tabnet_type)
		
		for i, (train_index, val_index) in enumerate(kf.split(x_train, y_train)):
			if (problem == 'classification'):
				unsupervised_model = TabNetPretrainer(**tabnet_params)
				tabnet_model = TabNetClassifier(**tabnet_params)
			elif (problem == 'regression'):
				unsupervised_model = TabNetPretrainer(**tabnet_params)
				tabnet_model = TabNetRegressor(**tabnet_params)
			else:
				pring('[ERROR] Unknown problem: {}'.format(problem))
				quit()
			
			x_tr = x_train[train_index]
			x_val = x_train[val_index]
			y_tr = y_train[train_index]
			y_val = y_train[val_index]
			
			unsupervised_model.fit(
				x_tr,
				eval_set=[x_val],
				patience=300,
				max_epochs=5000,
				pretraining_ratio=0.8
			)
			
			tabnet_model.fit(
				x_tr, y_tr,
				eval_set=[(x_val, y_val)],
				eval_metric=[fit_params['eval_metric']],
				batch_size=fit_params['batch_size'],
				virtual_batch_size=fit_params['virtual_batch_size'],
				patience=300,
				max_epochs=5000,
				from_unsupervised=unsupervised_model
			)
			
			self.tabnet_models.append(tabnet_model)
			prediction = tabnet_model.predict(x_val)
			if (problem == 'classification'):
				scores.append(accuracy_score(y_val, prediction))
			elif (problem == 'regression'):
				scores.append(mean_squared_error(y_val, prediction))
			else:
				pring('[ERROR] Unknown problem: {}'.format(problem))
				quit()
			
			if (i == 0):
				feature_importances = tabnet_model.feature_importances_.copy()
			else:
				feature_importances = np.vstack((feature_importances, tabnet_model.feature_importances_))
		
		print(scores)
		print(np.mean(scores))
		
		return scores, feature_importances
	
	def inference(self, x_test):
		for i, tabnet_model in enumerate(self.tabnet_models):
			if (i == 0):
				prediction = tabnet_model.predict(x_test)
			else:
				prediction = np.vstack((prediction, tabnet_model.predict(x_test)))
		
		return prediction

