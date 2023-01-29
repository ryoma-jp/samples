# FairMOT 実行例

## 事前準備

```
$ cd docker
$ docker-compose build
```

## 実行手順

### Installation

```
$ cd docker
$ docker-compose run fair_mot_env /bin/bash
# cd /work
# git clone https://github.com/ifzhang/FairMOT
# cd FairMOT
# pip install cython==0.29.33
# pip install -r requirements.txt
# git clone -b pytorch_1.7 https://github.com/ifzhang/DCNv2.git
# cd DCNv2
# ./make.sh
# cd ..
# mkdir models
# cd models
# wget https://code.ornl.gov/thorn/thorn-model-zoo/-/raw/main/fairmot_dla34.pth
# cd ../src
# python demo.py mot --load_model ../models/fairmot_dla34.pth --input-video ../videos/MOT16-03.mp4 --conf_thres 0.4
```

### Data preparation

* Dataset List
  * [Sample Movie](https://github.com/ifzhang/FairMOT/tree/master/videos)
  * [Crowd Human](https://www.crowdhuman.org/download.html)
    * Google Driveからのダウンロード
  * [MOT20](https://motchallenge.net/data/MOT20/)
    * 上記リンクから直接ダウンロード

## Reference

* [Thorn-Model-Zoo](https://code.ornl.gov/thorn/thorn-model-zoo)
