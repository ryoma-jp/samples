#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import numpy as np

#---------------------------------
# 関数
#---------------------------------
def get_label_index(label, onehot=True):
	if (onehot):
		label = np.argmax(label, axis=1)
	n_category = max(label)+1
	
	return np.array([np.arange(len(label))[label==i] for i in range(n_category)])
