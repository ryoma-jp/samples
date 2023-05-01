# ファイルをダウンロードするプログラムのサンプル

サイズの小さなファイルは``requests.get(url).content``でダウンロードするのが通常だが，サイズが大きなファイルば分割してダウンロードする必要がある．

ダウンロード対象として，機械学習で使用する[COCO Dataset](https://cocodataset.org/#download)をダウンロードする．  
一括ダウンロードとして``2017 Train/Val annotations [241MB]``を，分割ダウンロードとして``2017 Train images [118K/18GB]``を例に挙げる．

## 使い方

### 前準備

```
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec --user $UID file_download bash
$ cd /work
```

### 実行

#### 一括ダウンロード

```
$ python3 file_download.py --file_size small
```

#### 分割ダウンロード

T.B.D

## 参照

* [Pythonで作るHTTP分割ダウンロードするやつ](https://qiita.com/johejo/items/398f7208ebc2bc5a4724)


