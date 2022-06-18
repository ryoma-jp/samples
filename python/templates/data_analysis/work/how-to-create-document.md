# Sphinxドキュメント生成手順

1. reSTファイルの生成  
Project, Author部分は適宜修正
    ```
    $ sphinx-apidoc -F -H Project -A Author -o ./docs ./lib
    ```
1. conf.pyの編集  
下記3行のコメントを外す
    ```
    # import os
    # import sys
    # sys.path.insert(0, '/tf/work/lib')
    ```
extensionsに```sphinx.napoleon```を追加する
    ```
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.todo',
        'sphinx.ext.napoleon'     ←★この行を追加
    ]
    ```
変数```html_theme```で好みのテーマを設定する
    ```
    html_theme='nature'
    ```
1. HTMLドキュメント生成
    ```
    $ sphinx-build docs docs/html
    ```

## 参照

* [SphinxでPython docstringからドキュメントを自動生成する](https://helve-blog.com/posts/python/sphinx-documentation/)
* [Sphinxに組み込まれているテーマ](https://water2litter.net/pisco/doc/built_in_theme.html)

