# データセットの粒度(Granularity)算出サンプル

## 概要

* データセットの粒度(Granularity)算出サンプル

## 実行手順

	$ cd docker  
	$ docker build -t measuring_dataset_granularity/tensorflow:21.03-tf2-py3 .  
	$ ./docker_run.sh  
	# cd /work  
	# ./run.sh  

## 補足

* WSLでCIFAR-10のダウンロードに失敗する場合
DNSの名前解決に失敗している可能性があり，/etc/resolv.confに記載されているnameserverを「8.8.8.8」（Google Public DNS）に設定すると解決する場合があります

## 参考

* [Measuring Dataset Granularity](https://arxiv.org/abs/1912.10154)
* [WSL2から起動したDockerコンテナ内からaptが失敗する問題の対策](https://qiita.com/ryoma-jp/items/31cfc587e24db94953be)
* [Google Public DNS](https://developers.google.com/speed/public-dns)


