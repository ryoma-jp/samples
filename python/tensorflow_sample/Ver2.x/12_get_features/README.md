# モデルの中間層(特徴量)を抽出するサンプルプログラム

TensorFlowではロードしたモデルに対し，``layers``で各レイヤのインスタンスの取得や操作をすることができる．

モデルの定義方法により``layers``で取得できる単位がオペレーションであったりFunctional Layerであったりする．
Functional Layerに対しては``get_config()``を用いてFunctional Layerの情報を取得することが可能であるが，必ずしもオペレーションレベルの構造を取得できるとは限らない．

本サンプルプログラムでは，中間層の値を取得できる例とできない例を示す．

詳細な解説はこちら → []()

## 中間層の値を取得できるモデル例

### 実行手順

```
# python3 simple_cnn_saved_model.py
```


## 中間層の値を取得できないモデル例(YOLOv3)

### 実行手順

```
./run_yolov3.sh
```

### 中間層の値を取得できない要因

モデルを定義する際，中間層に``Input``オブジェクトを指定すると中間層の値を取得できない．  
厳密には，中間層の値を取得するために，定義した``Input``をモデルのInput Tensorとして与えなければならないが，この値が中間層の出力である為，推論前に値を設定することができない．

```
ValueError: Graph disconnected: cannot obtain value for tensor KerasTensor(type_spec=TensorSpec(shape=(None, None, None, 3), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'") at layer "conv2d". The following previous layers were accessed without issue: []
```

## 中間層の値を取得できないモデル例(CenterNetHourGlass104)

### 実行手順

```
python3 hourglass.py
```

### 中間層の値を取得できない要因

TensorFlow Hubからロードしたモデルは``_UserObject``であり，LayersModelクラスのインスタンスとして読み込むことができない．

```
AttributeError: '_UserObject' object has no attribute 'summary'
```
