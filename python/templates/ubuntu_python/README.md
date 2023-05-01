# UbuntuベースのPython環境

UbuntuをベースとしたPython環境のテンプレート

## 使い方

### 前準備

```
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec --user $UID ubuntu_python bash
$ cd /work
```

### テストプログラムの実行

```
$ python3 ubuntu_python.py
```


