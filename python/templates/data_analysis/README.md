# データ分析環境テンプレート

# ディレクトリ構成
```
.
├── data
├── docker
│   ├── Dockerfile
│   └── docker_run.sh
├── README.md
└── work
    └── lib
```

|directory/file|description|
|:--|:--|
|data|データセットを格納する|
|docker/Dockerfile|本プロジェクトを実行するための環境構築用Dockerfile|
|docker/docker_run.sh|Docker Containerを起動するためのスクリプト|
|README.md|本ファイル|
|work|本ディレクトリ直下にメインプログラムやスクリプト等を置く|
|work/lib|分析・学習用の自作ライブラリを格納する|

## 分析環境の実行手順

1. ```data```ディレクトリにデータセットを置く
2. Jupyterを起動する

