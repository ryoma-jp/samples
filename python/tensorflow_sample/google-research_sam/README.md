# TensorFlowでのSAMのCIFAR-10学習サンプル

## 概要

* 2021.4.17時点でのPaper with Code Image Classification on CIFAR-10のSOTAである，SAM: Sharpness-Aware Minimization for Efficiently Improving Generalizationの学習サンプル  
![Image Classification on CIFAR-10](https://github.com/ryoma-jp/samples/blob/master/python/tensorflow_sample/google-research_sam/figures/210417_image_classification_on_cifar-10.png)!

## 実行手順

### Dockerイメージ作成，コンテナ起動
<pre>
$ docker build -t google-research_sam/tensorflow:21.03-tf2-py3 .
$ ./docker_run.sh
</pre>

### 環境設定，学習実行
<pre>
# cd /work
# ./01_create_env.sh
# ./02_run.sh
</pre>

### 補足

手元の環境(GeForce RTX 2070 SUPER)では，1EPOCHの学習に約4分を要し，デフォルトの1800EPOCHでは学習完了まで約5日かかる．
学習時GPU使用率はほぼ100%を維持し，温度は80度程度まで上昇し非常に負荷が高い状態となる為，1800EPOCHの学習は未実施．

