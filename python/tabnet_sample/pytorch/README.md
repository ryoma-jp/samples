# TabNetのサンプル

## 概要

* TabNetの学習サンプル

## 実行手順

### KaggleのTitanic Datasetの二値分類サンプル

#### KaggleのTitanicコンペからtrain.csvとtest.csvをダウンロードする

* ダウンロードURL: https://www.kaggle.com/c/titanic/data
* 格納先: ./dataset/titanic

#### スクリプトを実行する

	$ cd docker  
	$ docker build -t tabnet/pytorch:21.04-py3  .  
	$ ./docker_run.sh  
	# cd /work  
	# vim run.sh
		DATASET_TYPEをTitanicに変更
	# ./run.sh  

### ロボットの関節位置/速度/加速度からトルクを推定するSARCOS Datasetの回帰サンプル

#### スクリプトを実行する

	$ cd docker  
	$ docker build -t tabnet/pytorch:21.04-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# vim run.sh
		DATASET_TYPEをTitanicに変更
	# ./run.sh  

### 参考

* [TabNetとは一体何者なのか？](https://zenn.dev/sinchir0/articles/9228eccebfbf579bfdf4)
* [TabNetをKaggleに使ってみる](https://qiita.com/t-smz/items/6e5d6c10aba7a8e3f991)
* [TabNet Titanic](https://www.kaggle.com/tamreff3290/tabnet-titanic)
* [pytorch-tabnet](https://pypi.org/project/pytorch-tabnet/)
* [The SARCOS data](http://www.gaussianprocess.org/gpml/data/)
* [TabNet: Attentive Interpretable Tabular Learning](https://arxiv.org/pdf/1908.07442.pdf)

