# Bootstrap Djangoの実装サンプル

Webページのビューやフォーム毎のDjango実装サンプルを紹介する
CSSフレームワークにはBootstrapを使用する

## サーバ起動手順

```
$ ./run_server.sh
```

## 追加予定の機能

* [x] 表
* [x] チェックボックス
* [x] ラジオボタン
* [x] ドロップダウンボタン
* [x] サイドバー
* [x] ファイルアップロード
* [ ] グラフ
* [x] 画像表示

## OSS利用について

本コードには下記のOSSを利用している

* static/css/dashboard.css
  * [Bootstrap公式のExamples](https://getbootstrap.jp/docs/5.0/examples/)からダウンロード
    * https://github.com/twbs/bootstrap/releases/download/v5.0.2/bootstrap-5.0.2-examples.zip


## Reference

* [Introduction](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
  * レイアウトやコンポーネントなどのコードをコピーできる
* [integrity 属性を使った改ざん検知](https://mgng.mugbum.info/1468)
  * ソースのハッシュ値を取得する方法  
  ```
    $ cat FILENAME | openssl dgst -sha384 -binary | openssl base64 -A
  ```
* 静的ファイルの扱い方
  * [Djangoにおける静的ファイル(static file)の取り扱い](https://qiita.com/saira/items/a1c565c4a2eace268a07)
  * [Django staticファイル まとめ](https://qiita.com/okoppe8/items/38688fa9259f261c9440)
  * 静的ファイルの読み込みで404エラーが出る場合  
    → STATICFILES_DIRSを設定する
* [スペース設定](https://getbootstrap.com/docs/5.1/utilities/spacing/)
* レイアウト
  * [Flex](https://getbootstrap.com/docs/5.1/utilities/flex/)
  * [Comumns](https://getbootstrap.com/docs/5.1/layout/columns/)


