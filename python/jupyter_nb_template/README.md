# DockerでのJupyter Notebook環境

## 概要

* 一般的なPython環境(GPU非対応=GPU_OFF)のものと，GPU対応(GPU_ON)の二種類を紹介する
	* 一般的なPython環境は「jupyter/scipy-notebook」 → Dockerfile_gpu_off
	* GPU対応(TensorFlow)は「tensorflow/tensorflow:latest-gpu-jupyter 」 → Dockerfile_gpu_on
	* Dockerの実行はdocker_run_*.shで選択する
		* GPU_OFF: docker_run_gpu_off.sh
		* GPU_ON : docker_run_gpu_on.sh

## 実行手順

	docker_run_*.shで起動後，
		GPU_OFF → http://localhost:10000
		GPU_ON  → http://localhost:10001
	へブラウザでアクセスし，コンソールに表示されるトークン部分をコピペしてログインする

## 参照

* [Dockerを使って5分でJupyter環境を構築する](https://qiita.com/fuku_tech/items/6752b00770552bf4f46b)
* [TensorFlow Docker のイメージをダウンロードする](https://www.tensorflow.org/install/docker?hl=ja#download_a_tensorflow_docker_image)


