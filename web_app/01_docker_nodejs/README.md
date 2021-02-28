# Description

DockerでのNode.js Webアプリケーションのサンプル．


# Usage

* サーバを起動するターミナルで下記を実行
<pre>
$ cd web_app/01_docker_nodejs
$ ./docker_build.sh
$ ./docker_run.sh
# node server.js
</pre>

* クライアント用の端末で下記を実行
	* GET
	<pre>
	$ curl -i localhost:8080
	</pre>
	* POST
	<pre>
	$ curl -X POST -H "Content-Type: application/json" -d '{"test":"test"}' localhost:8080/
	</pre>

# Reference

* [Node.js Web アプリケーションを Docker 化する](https://nodejs.org/ja/docs/guides/nodejs-docker-webapp/)
* [node.js + expressでPOSTを受け取る & POSTパラメータをJSONで取得する](https://qiita.com/ktanaka117/items/596febd96a63ae1431f8)
* [Node.js + Express でPOSTデータを取得後、WebAPIへ問い合わせる](https://qiita.com/ktanaka117/items/596febd96a63ae1431f8)





