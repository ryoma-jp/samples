#! -*- coding: utf-8 -*-

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import pandas as pd

#---------------------------------
# 定数定義
#---------------------------------

#---------------------------------
# 関数
#---------------------------------
def null_count(train_data, test_data):
	print('<< null count: train_data >>')
	print(pd.isnull(train_data).sum())
	print('<< null count: test_data >>')
	print(pd.isnull(test_data).sum())
	
	return
	
def load_titanic(dataset_dir, data_cleansing=True):
	# --- load train.csv ---
	train_data = pd.read_csv(os.path.join(dataset_dir, 'train.csv'))
	
	# --- load test.csv ---
	test_data = pd.read_csv(os.path.join(dataset_dir, 'test.csv'))
	
	# --- data cleansing ---
	if (data_cleansing):
		null_count(train_data, test_data)
		# --- Drop labels ---
		#  * Cabin: Too many lost data
		#  * Ticket: Value is too complex
		train_data.drop(labels=["Cabin", "Ticket"], axis=1, inplace=True)
		test_data.drop(labels=["Cabin", "Ticket"], axis=1, inplace=True)
		
		# --- Data complement ---
		#  * Age: median
		#  * Embarked: replace value(C->0, S->1, Q->2) and fillna median 
		#  * Sex: replace value(male->0, female->1)
		#  * Fare: median(only test_data)
		train_data['Age'].fillna(round(train_data['Age'].median()), inplace=True)
		test_data['Age'].fillna(round(test_data['Age'].median()), inplace=True)
		
		train_data.loc[train_data['Embarked']=='C', 'Embarked'] = 0
		train_data.loc[train_data['Embarked']=='S', 'Embarked'] = 1
		train_data.loc[train_data['Embarked']=='Q', 'Embarked'] = 2
		train_data['Embarked'].fillna(round(train_data['Embarked'].median()), inplace=True)
		test_data.loc[test_data['Embarked']=='C', 'Embarked'] = 0
		test_data.loc[test_data['Embarked']=='S', 'Embarked'] = 1
		test_data.loc[test_data['Embarked']=='Q', 'Embarked'] = 2
		test_data['Embarked'].fillna(round(test_data['Embarked'].median()), inplace=True)
		
		train_data.loc[train_data['Sex']=='male', 'Sex'] = 0
		train_data.loc[train_data['Sex']=='female', 'Sex'] = 1
		test_data.loc[test_data['Sex']=='male', 'Sex'] = 0
		test_data.loc[test_data['Sex']=='female', 'Sex'] = 1
		
		test_data['Fare'].fillna(round(test_data['Fare'].median()), inplace=True)
		
		null_count(train_data, test_data)
		train_labels = train_data['Survived']

	else:
		train_labels = train_data['Survived']
	
	return train_data, train_labels, test_data



