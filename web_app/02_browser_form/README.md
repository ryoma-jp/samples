# Description

DockerでのNode.js Webアプリケーションのサンプル．
ブラウザのフォームからのPOST送信し，フォームに入力したデータをコンソールに表示する．

# Usage

* サーバを起動するターミナルで下記を実行
<pre>
$ cd web_app/01_docker_nodejs
$ ./docker_build.sh
$ ./docker_run.sh
# node server.js
</pre>

* ブラウザで下記にアクセスし，フォームへデータを入力してSubmitボタンをクリックするとサーバ側のコンソールにフォームに入力したデータが表示される  
http://localhost:8080

# Reference

* [body-parser で フォームからの POST データを受け取る方法](https://nodejs.keicode.com/nodejs/body-parser-form.php)





