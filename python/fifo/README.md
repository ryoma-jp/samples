# FIFOを用いたプロセス間通信

## 概要

* main.pyからワーカプロセスをバックグラウンドで起動し，FIFOを介して制御するプロセス間通信サンプル

## 実行手順

### Docker Image生成

```
$ cd docker
$ docker build --network=host -t fifo/tensorflow:21.03-tf2-py3 .
$ docker_run.sh
```

### ワーカプロセスの起動

```
# cd /work
# ./run_open.sh
```

### ワーカプロセスの終了

```
# cd /work
# ./run_exit.sh <pid>
    ※<pid>には./run_open.shで生成されたワーカプロセスのPIDを指定する
```

## 制限事項

* Linux環境でのみ動作

## 参照

* [Pythonのsubprocessモジュールでコマンドをバックグラウンドで実行する方法を現役エンジニアが解説【初心者向け】](https://techacademy.jp/magazine/36078)
