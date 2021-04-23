# Deep Neural Networkの演算プログラムのサンプル

## 概要

* TensorFlow，汎用CPU実装，ARM向け実装の処理時間比較用のサンプルプログラム

## 環境構築，Dockerコンテナ起動

<pre>
$ docker build -t dnn/tensorflow:21.03-tf2-py3 .
$ ./docker_run.sh
# cd /work
</pre>

## 実行手順

### TensorFlowでのCIFAR-10モデル学習

<pre>
# cd tensorflow
# ./run.sh
</pre>

