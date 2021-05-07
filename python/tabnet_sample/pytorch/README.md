# TabNetのサンプル

## 概要

* Titanicデータセットを用いたTabNetのサンプル

## 実行手順

### KaggleのTitanicコンペからtrain.csvとtest.csvをダウンロードする

* ダウンロードURL: https://www.kaggle.com/c/titanic/data
* 格納先: ./dataset/titanic

### スクリプトを実行する

	$ cd docker  
	$ docker build -t tabnet/pytorch:21.03-tf2-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# ./run.sh  


### 参考

* [TabNetとは一体何者なのか？](https://zenn.dev/sinchir0/articles/9228eccebfbf579bfdf4)
* [TabNetをKaggleに使ってみる](https://qiita.com/t-smz/items/6e5d6c10aba7a8e3f991)
* [TabNet Titanic](https://www.kaggle.com/tamreff3290/tabnet-titanic)
* [pytorch-tabnet](https://pypi.org/project/pytorch-tabnet/)


