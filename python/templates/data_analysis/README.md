# データ分析環境テンプレート

# ディレクトリ構成
```
.
├── data
├── docker
│   ├── docker-compose.yml
│   └── tensorflow
│       └── Dockerfile
├── README.md
└── work
    ├── how-to-create-document.md
    ├── lib
    │   ├── data_loader.py
    │   └── metrics.py
    └── nb_samples
        └── table_data-lightgbm
            ├── dataset
            ├── models
            ├── table_data_analysis_template.ipynb
            ├── table_data_inference_template.ipynb
            ├── table_data_preprocessing_template.ipynb
            └── table_data_training_template.ipynb
```

|directory/file|description|
|:--|:--|
|data|データセットを格納する|
|docker/docker-compose.yml|アプリケーションサービスの設定ファイル|
|docker/tensorflow/Dockerfile|TensorFlow用アプリケーション向けのDockerfile|
|README.md|本ファイル|
|work|本ディレクトリ直下にメインプログラムやスクリプト等を置く|
|work/lib|分析・学習用のライブラリを格納する|
|work/how-to-create-document.md|Sphinxを用いたドキュメント生成方法|
|work/nb_samples/table_data-lightgbm|テーブルデータの分析サンプル。学習モデルはLightGBM|
|work/nb_samples/table_data-lightgbm/dataset|前処理で抽出した学習用データセットの保存用ディレクトリ|
|work/nb_samples/table_data-lightgbm/models|学習済みモデルを保存する|
|work/nb_samples/table_data-lightgbm/table_data_analysis_template.ipynb|データ分析処理用テンプレート|
|work/nb_samples/table_data-lightgbm/table_data_inference_template.ipynb|テーブルデータ推論用テンプレート|
|work/nb_samples/table_data-lightgbm/table_data_preprocessing_template.ipynb|テーブルデータ前処理用テンプレート|
|work/nb_samples/table_data-lightgbm/table_data_training_template.ipynb|テーブルデータ学習用テンプレート|

## 分析環境の実行手順

1. ```data```ディレクトリにデータセットを置く
2. Jupyterを起動する

## よくある問題と対策

* ```load_dataset()```でカリフォルニア住宅価格予測用データセットがダウンロードできない
  * Dockerコンテナ内の/etc/resolv.confに記載されているnamespaceを8.8.8.8に変更する

