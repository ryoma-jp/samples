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
    ├── dataset
    ├── how-to-create-document.md
    ├── lib
    │   ├── data_loader.py
    │   └── metrics.py
    ├── table_data_preprocessing_template.ipynb
    └── table_data_training_template.ipynb
```

|directory/file|description|
|:--|:--|
|data|データセットを格納する|
|docker/Dockerfile|本プロジェクトを実行するための環境構築用Dockerfile|
|docker/docker_run.sh|Docker Containerを起動するためのスクリプト|
|README.md|本ファイル|
|work|本ディレクトリ直下にメインプログラムやスクリプト等を置く|
|work/dataset|前処理で抽出した学習用データセットの保存用ディレクトリ|
|work/lib|分析・学習用の自作ライブラリを格納する|
|work/table_data_preprocessing_template.ipynb|テーブルデータ前処理用テンプレート|
|work/table_data_training_template.ipynb|テーブルデータ学習用テンプレート|

## 分析環境の実行手順

1. ```data```ディレクトリにデータセットを置く
2. Jupyterを起動する

