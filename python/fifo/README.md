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

#### ブロッキング版

ワーカプロセス側でFIFOのopenをブロックしてデータを待つ方式の実装サンプル

```
# cd /work
# ./run_open.sh
```

#### ノンブロッキング版

ワーカプロセス側でFIFOのopenをノンブロッキングで待つ方式の実装サンプル
※1[sec]毎にFIFOの状態をポーリング

```
# cd /work
# ./run_open_non-blocking.sh
```

### ワーカプロセスの終了

```
# cd /work
# ./run_exit.sh <pid>
    ※<pid>には./run_open.shで生成されたワーカプロセスのPIDを指定する
```

## 制限事項

* Linux環境でのみ動作

## 参考：実行ログ

### ブロッキング版

```
root@448911cca8f0:/work# ./run_open.sh
args.command : open
args.pid : open
args.list : False
args.non_blocking : False
59fe25c61d436cdf6fcccdc8cf9e980373d2132e18c377909a08eccdc8cbcce1
{825: '59fe25c61d436cdf6fcccdc8cf9e980373d2132e18c377909a08eccdc8cbcce1'}
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   9456  7448 pts/0    Ss   Jan01   0:00 /bin/bash
root       814  0.0  0.0   5864  3800 pts/0    S+   04:26   0:00 /bin/bash ./run_open.sh
root       825  0.0  0.0  12128  7856 pts/0    R+   04:26   0:00 python sub_proc.py
root       826  0.0  0.0   7652  3244 pts/0    R+   04:26   0:00 ps -aux
args.non_blocking : False
args.command : None
args.pid : None
args.list : True
args.non_blocking : False
{
    "825": "59fe25c61d436cdf6fcccdc8cf9e980373d2132e18c377909a08eccdc8cbcce1"
}
root@448911cca8f0:/work# ./run_exit.sh 825
args.command : exit
args.pid : exit
args.list : False
args.non_blocking : False
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   9456  7448 pts/0    Ss   Jan01   0:00 /bin/bash
root       828  0.0  0.0   5864  3816 pts/0    S+   04:26   0:00 /bin/bash ./run_exit.sh 825
root       837  0.0  0.0   7652  3172 pts/0    R+   04:26   0:00 ps -aux
args.command : None
args.pid : None
args.list : True
args.non_blocking : False
{}
root@448911cca8f0:/work# cat /tmp/subproc/59fe25c61d436cdf6fcccdc8cf9e980373d2132e18c377909a08eccdc8cbcce1/log/log.txt
2022-01-02 04:26:27,752     INFO exit
root@448911cca8f0:/work#
```

### ノンブロッキング版

```
root@448911cca8f0:/work# ./run_open_non-blocking.sh
args.command : open
args.pid : open
args.list : False
args.non_blocking : True
5e0737ddcdcf00d4515224c267feee9af5b086bce45660c01d3c05e51fe83f3d
{853: '5e0737ddcdcf00d4515224c267feee9af5b086bce45660c01d3c05e51fe83f3d'}
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   9456  7448 pts/0    Ss   Jan01   0:00 /bin/bash
root       842  0.0  0.0   5864  3748 pts/0    S+   04:27   0:00 /bin/bash ./run_open_non-blocking.sh
root       853  0.0  0.0  12132  7960 pts/0    R+   04:27   0:00 python sub_proc.py --non-blocking
root       854  0.0  0.0   7652  3168 pts/0    R+   04:27   0:00 ps -aux
args.non_blocking : True
args.command : None
args.pid : None
args.list : True
args.non_blocking : False
{
    "853": "5e0737ddcdcf00d4515224c267feee9af5b086bce45660c01d3c05e51fe83f3d"
}
root@448911cca8f0:/work# ./run_exit.sh 853
args.command : exit
args.pid : exit
args.list : False
args.non_blocking : False
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   9456  7448 pts/0    Ss   Jan01   0:00 /bin/bash
root       856  0.0  0.0   5864  3808 pts/0    S+   04:27   0:00 /bin/bash ./run_exit.sh 853
root       865  0.0  0.0   7652  3164 pts/0    R+   04:27   0:00 ps -aux
args.command : None
args.pid : None
args.list : True
args.non_blocking : False
{}
root@448911cca8f0:/work# cat /tmp/subproc/5e0737ddcdcf00d4515224c267feee9af5b086bce45660c01d3c05e51fe83f3d/log/log.txt
2022-01-02 04:27:27,634     INFO FIFO is empty
2022-01-02 04:27:28,636     INFO FIFO is empty
2022-01-02 04:27:29,637     INFO FIFO is empty
2022-01-02 04:27:30,639     INFO FIFO is empty
2022-01-02 04:27:31,640     INFO FIFO is empty
2022-01-02 04:27:32,642     INFO FIFO is empty
2022-01-02 04:27:33,643     INFO FIFO is empty
2022-01-02 04:27:34,645     INFO exit
root@448911cca8f0:/work#
```


## 参照

* [Pythonのsubprocessモジュールでコマンドをバックグラウンドで実行する方法を現役エンジニアが解説【初心者向け】](https://techacademy.jp/magazine/36078)
* [O_NONBLOCK does not raise exception in Python](https://stackoverflow.com/questions/38843278/o-nonblock-does-not-raise-exception-in-python)
* [exception BlockingIOErro](https://docs.python.org/ja/3/library/exceptions.html#BlockingIOError)
* [os.open](https://docs.python.org/ja/3/library/os.html#os.open)
* [os.read](https://docs.python.org/ja/3/library/os.html#os.read)
