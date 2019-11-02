# 探索アルゴリズムのサンプル

## 概要

* 探索アルゴリズムのサンプル
* 10000のランダムな整数群から10000の整数すべての登録・探索する時間を測定
* 下記のアルゴリズムを実装
	* 線形探索	linear_search()  
		* データの登録はデータが現れた順にリストへ登録  
		* 探索はリストの先頭から順番に実施  
	* 2分探索	binary_search()  
		* データの登録はデータが昇順になるようにソートして登録  
		* 探索はリストの2分割を反復  
	* ハッシュ探索	hash_search()  
		* データの登録はハッシュ関数の戻り値をもとにハッシュ表へ登録  
		* 探索はハッシュ関数の戻り値をもとにハッシュ表を参照  
		* 衝突(collision)発生時のシノニム(synonym)格納方法  
			* チェイン法 … 衝突しても同じ位置に複数のデータを格納する  
			* オープンアドレス法 … 衝突したとき，新しい格納位置を計算によって求め直す  

## 実行手順

	$ make
	$ mkdir result
	$ ./search ./result

## 参考

* http://www.yamaguti.comp.ae.keio.ac.jp/japanese/2017-lecture-A/5before%E6%8E%A2%E7%B4%A2(2017-10-27).pdf
* http://web.wakayama-u.ac.jp/~manda/alg/alg10.pdf
* http://www.info.kochi-tech.ac.jp/k1sakai/Lecture/ALG/2012/ALG2012-5.pdf
* https://www.kunihikokaneko.com/cc/program/hash.pdf

