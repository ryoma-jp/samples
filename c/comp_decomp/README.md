# 圧縮・解凍アルゴリズムのサンプル

## 概要

* 下記の圧縮方式のサンプルプログラム
	* ランレングス圧縮
	* ハフマン符号  
* ビット列に対して圧縮するバイナリデータ圧縮とバイト列に対して圧縮するバイトデータ圧縮の2種類のサンプルを実装する  
	* 画像(BMPなどのRAWデータ)やテキスト等，8bit単位のデータの圧縮はバイトデータ圧縮を使用し，データに単位のないものはバイナリデータ圧縮を使用する
* 各圧縮・解凍モジュールは圧縮する単位を引数で指定できるインターフェースとして実装し，main関数から呼び出す部分のサンプルとしてバイナリデータ圧縮とバイトデータ圧縮の2種類を表現する
* [T.B.D] 圧縮したデータが何bit単位で圧縮したものか分からなくなると解凍できなくなるので，圧縮後データに圧縮単位を示すヘッダをつければ解凍部分は共通化できる  
	* ヘッダの分，圧縮率が悪くなる点がトレードオフ

## 実行手順

### コンパイル
	$ make

### エンコード
	$ ./comp_decomp --enc input.bin output.bin

### デコード
	$ ./comp_decomp --dec input.bin output.bin
