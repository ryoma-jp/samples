# CSG(Cumulative Spectral Gradient)の実行サンプル

## 概要

* CSGを用いたデータセットの複雑度を計測するサンプル

## 実行手順

	$ cd docker  
	$ docker build -t csg_sample/tensorflow:21.03-tf2-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# ./run.sh  


# 参考

* [学習をせずにCNNの精度がわかる？データセットの複雑度を測る新たな指標CSGの登場！](https://ai-scholar.tech/articles/others/csg-ai-337)
* [Cumulative Spectral Gradient (CSG) metric](https://github.com/Dref360/spectral_metric)
