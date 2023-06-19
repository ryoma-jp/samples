# TensorFlowの実装サンプルを動かす仮想環境

## ビルド方法

1. NVIDIAのDeveloperサイトからインストール用パッケージ``cudnn-local-repo-ubuntu2004-8.9.2.26_1.0-1_amd64.deb``取得する
1. Dockerイメージをビルドする  
    ```
    $ docker build -t tf_sample_v2/tensorflow:21.03-tf2-py3 .
    ```

## コンテナの起動

```
$ ./docker_run.sh
```
