# globモジュールを用いてファイル探索しリストに保存する

## 概要

* globモジュールでファイルのリストは取得できるが，取得順はランダム
* 文字列順でソートするにはsortedを用いる
* sortedの引数keyに，os.path.getmtimeを指定すればファイルの生成順，os.path.getsizeを指定すればファイルサイズ順にソートできる
* ファイル名に連番が振られている場合は，数値でソートできるように独自で定義する必要がある(numericalSort)
* このサンプルの実装では，正規表現を用いて数値でsplitし，数値が格納されるparts[1], parts[3], ... をintでキャストする
* 文字列ソートと数値(int)のソートの違い
	* 文字列ソート：'0', '1', '10', '2', '3', ...
	* 数値(int)ソート：0, 1, 2, 3, ...
* globモジュールの探索パスに'\*\*'を加え，recursive=Trueを指定すると再帰的にサブディレクトリ内を探索できる

## 実行手順

	$ cd input_files
	$ ./00_create_files.sh
	$ cd ..
	$ python3 glob_sample.py --search_dir ./input_files --output_dir ./result
	
	以下，必要に応じて
	$ cd input_files
	$ ./01_remove_files.sh
	$ cd ..

## 参考

* https://stackoverflow.com/questions/6773584/how-is-pythons-glob-glob-ordered
* https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python

