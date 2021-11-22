# 行列計算

## 概要

* 内積計算のNeon実装サンプル(ARM公式ドキュメントに記載のチュートリアルの動作確認)
* Aarch64で動作を確認

## 実行手順

### Aarch64オンボードでの実行

	$ make
	$ ./run.sh

### クロスコンパイル

	$ make -f Makefile_for_xc_aarch64

## 参照

* [Matrix multiplication example](https://developer.arm.com/documentation/102467/0100/Matrix-multiplication-example)
