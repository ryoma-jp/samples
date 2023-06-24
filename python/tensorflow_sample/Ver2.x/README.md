# TensorFlowの実装サンプル

## ディレクトリ構成

|ディレクトリ名|説明|
|:--|:--|
|00_docker|TensorFlowの実装サンプルを実行する仮想環境|
|01_mlp_mnist|FCモデルを用いたMNISTデータセットの数字識別モデルの学習|
|02_cnn_cifar10|CNNモデルを用いたCIFAR-10データセットの画像識別モデルの学習|
|03_resnet_cifar10|ResNetを用いたCIFAR-10データセットの画像識別モデルの学習|
|04_compare_models|FCモデル，CNNモデル，ResNetのモデル間比較|
|05_data_augmentation|DataAugmentationパラメータ毎の画像識別モデルの精度比較|
|06_optimizer|Optimizer毎の画像識別モデルの精度比較|
|07_parameter_tunings|ハイパーパラメータ毎の画像識別モデルの精度比較|
|08_resnet_initializer|ResNetのパラメータ初期化方式別の画像識別モデルの精度比較|
|09_data_normalization|データの正規化方式別の画像識別モデルの精度比較|
|10_generalization|01～09のパラメータ組み合わせ（学習スクリプト整備）|
|11_terminate|モデルの学習を中断するサンプルプログラム|
|12_get_features|AIモデルの中間層を抽出するサンプルプログラム(動くものと動かないものを色々)|


