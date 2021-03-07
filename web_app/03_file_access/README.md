# Description

DockerでのNode.js Webアプリケーションのサンプル．
ブラウザのフォームからのPOST送信し，フォームに入力したデータをjson形式で保存する．

	1. ブラウザからフォームにuser, age, phone を入力
	2. フォームに入力されたデータをSubmitでPOST送信
	3. サーバがデータを受信し，user名でディレクトリを作成
	4. <user名>/user_info.jsonにuser, age, phone を保存

# Usage

* サーバを起動するターミナルで下記を実行
<pre>
$ cd web_app/03_file_access
$ ./docker_build.sh
$ ./docker_run.sh
# node server.js
</pre>

* ブラウザで下記にアクセスし，フォームへデータを入力してSubmitボタンをクリックするとサーバ側のコンテナ内にフォームに入力したデータが保存される  
http://localhost:8080  
<pre>
root@69a212866dc0:/usr/src/app# ls users/
root@69a212866dc0:/usr/src/app# node server.js
Running on http://0.0.0.0:8080
{ name: 'name', age: 'age', phone: 'phone' }
users/name
/usr/src/app/users/name/user_info.json
/usr/src/app
[INFO] save user_info done
^C
root@69a212866dc0:/usr/src/app# ls users/
name
root@69a212866dc0:/usr/src/app# cat users/name/user_info.json
{
        "name": "name",
        "age": "age",
        "phone": "phone"
}root@69a212866dc0:/usr/src/app#

</pre>


# Reference

* [[Node.js]パス文字列を結合する](https://tech.chakapoko.com/nodejs/file/pathjoin.html)
* [[Node.js] ファイルに書き込む様々な方法](https://blog.katsubemakito.net/nodejs/file-write)
* [Node.js でファイルを保存する方法](https://qiita.com/phi/items/b5ade0c2ecc58935e046)
* [【2019年6月版】fs.writeFile したら ERR_INVALID_CALLBACK ですって](https://qiita.com/koinori/items/7a69e0c0033bf61b44c8)
* [Request’s Past, Present and Future](https://github.com/request/request/issues/3142)
* [Alternative libraries to request](https://github.com/request/request/issues/3143)
* [axios](https://www.npmjs.com/package/axios)



