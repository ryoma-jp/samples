# FairMOT 実行例

## 事前準備

```
$ cd docker
$ docker-compose build
```

## 実行手順

```
$ cd docker
$ docker-compose run fair_mot_env /bin/bash
# cd work
# git clone https://github.com/ifzhang/FairMOT
# cd FairMOT
# pip install cython
# pip install -r requirements.txt
# git clone -b pytorch_1.7 https://github.com/ifzhang/DCNv2.git
# cd DCNv2
# ./make.sh
```
