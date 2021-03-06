## 参考チュートリアル

https://djangogirlsjapan.gitbook.io/workshop_tutorialjp/django_start_project

## pythonのインストール

https://www.python.org/

ターミナルで確認！

```iTerm
$ python3 --version
```

### Djangoのインストール

適当にディレクトリ作成
```
$ mkdir djangogirls
$ cd djangogirls
```
pythonのもともとパッケージで入っているvenv(virtual env)をつかって仮想環境を作成
※　今回は myvenv
```
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

コマンドプロンプトの上か横に、(myvenv)みたいな表示になれば大丈夫！
さぁさぁ、お待ちかねのDjangoのインストール
```
$ pip install --upgrade pip
$ pip install django==1.11  # => Djangoのインストール
```
Djangoのプロジェクトのはじめ(今回は、`mysite`)
```
$ django-admin startproject mysite .
```
以下のディレクトリ構成になっていればOK
```
djangogirls
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

`__init.py`の中身は空でも問題ありません。この`__init__.py`にimportしておきたいファイルを相対パスを使って書くことで、複数のファイルを一度にimportさせることも出来ます。
importの仕方 -> https://qiita.com/karadaharu/items/37403e6e82ae4417d1b3

`manage.py `はサイト管理用のスクリプトです。これで、他のものを一切インストールすることなく、コンピューター上でWebサーバーを動かすことができます。

`settings.py`は、サイトの設定ファイルです。

どこに手紙を配達するか番地を確認する郵便配達員の話を覚えていますか？ `urls.py`ファイルは、`urlresolver`をつかったURLのパターンのリストを含んでいます。

今は他のファイルについては無視しておきましょう。触ることはありません。間違って削除してしまわないようにさえしておけば大丈夫です！

### configuratinを変えよう
以下に変更
```mysite/settings.py
LANGUAGE_CODE = 'ja-JP'

TIME_ZONE = 'Asia/Tokyo'

USE_TZ = False
```

DBについて！

今回は、チュートリアルの乗っ取りながらやっているので
チュートリアルで扱う`sqlite3`を使います。

この部分があります！（テンプレでできてるはず）
```mysite/settings.py
  ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

...
```


```iTerm
$ python manage.py migrate
```

まぁ、`bundle exec rails db:migrate`と同じ意味じゃね？笑


```iTerm
(myvenv) ~/djangogirls$ python manage.py runserver
```

`bundle exec rails s`と同じ意味じゃね？笑

デフォルトのポート番号は、8000！
`localhost:8000`でアクセス可能！

### アプリケーション作成コマンド(この例 : blogアプリケーション)
```
(myvenv) ~/djangogirls$ python manage.py startapp blog
```

### 今のディレクトリ状況
```
    djangogirls
    ├── blog
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── db.sqlite3
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

アプリケーションを作成したら、Djangoにをそれを伝える必要がある！

それは、`mysite/settings.py`ファイルの中でやります。

`INSTALLED_APPS`のなかに`blog`を入れる。

`mysite/settings.py`

```
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',
    )
```

modelをつくると、今度はmigrationファイルの作成。

モデルで型などを定義したのちに`python manage.py makemigrations [モデル名]`を実行すると、

```
(myvenv) ~/djangogirls$ python manage.py makemigrations blog
Migrations for 'blog':
  0001_initial.py:
  - Create model Post
```

あとは、migrateを実行！(DBにmigrationファイルを読み込ませてテーブルやカラムを作成)

```
(myvenv) ~/djangogirls$ python manage.py migrate blog
Operations to perform:
  Apply all migrations: blog
Running migrations:
  Applying blog.0001_initial... OK
```

```
見て分かる通り、前回定義したPostモデルをimportしています。モデルをadminページで見れるようにするには、モデルをadmin.site.register(Post)で登録する必要があります。
```

```
$ python manage.py runserver
```
で確認！

http://127.0.0.1:8000/admin/ にアクセスすると、



となる！

これは、管理画面に入るためのユーザー(superuserという)のサインインを施している！

これに登録するには、以下のコマンドを打つ必要がある。


```
$ python manage.py createsuperuser
```

今回は

```
{
    username : admin
    email : admin@admin.com
    password : hogehoge
}
```

で作成！

admin画面についてもっと知りたければ、

https://docs.djangoproject.com/ja/1.11/ref/contrib/admin/​

### デプロイ

herokuにデプロイ！

まず、必要なファイルたち！
```
1. requirements.txt (あなたのサーバーにどんなPythonパッケージがインストールされる必要があるか、Herokuに伝えるもの)
2. Procfile  (このファイルが、どのコマンドを実行してウェブサイトをスタートするかHerokuに伝えます)
3. runtime.txt  (Pythonのバージョンを伝えるファイル！)
```

* まず、requirements.txtにかんして

`virtualenv`内で

```
$ pip install dj-database-url gunicorn whitenoise
インストールが終わったら、
$ pip freeze > requirements.txt
```

> 補足: pip freeze は、あなたのvirtualenvにインストール済みの全てのPythonライブラリを一覧にして出力します。そのpip freezeした出力先を、>の後に示しファイルに保存します。> requirements.txt を含まずに pip freeze だけで実行してみて、何が起こるか試してみるとよいでしょう。

そして、`requirements.txt`の最後の行に以下の行を追加しましょう。

```
psycopg2==2.5.4
```


* Procfile

```
web: gunicorn mysite.wsgi
```

このコマンドを実行することでデプロイすることを意味しています!


* runtime.txt

heroku用のpython の versionを指定するファイル！


* mysite/local_settings.py
`mysite/local_settings.py`が存在しないので、新しく作成し、以下を記述。


```
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
```

#### ここからは、既存のファイルの変更！

* `mysite/settings.py`に新しく以下を追記！

```
import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'staticfiles'

DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass
```

このファイルは、Herokuに必要な構成だけでなく、mysite/local_settings.pyファイルがある時にはローカルの設定にも重要な役割となります。

この部分は廃止！ -> どうやらversion の問題らしい、、、

        * `mysite/wsgi.py`に以下を追加！

        静的ファイルの配信用のコードである、以下を追加！

        ```
        from whitenoise.django import DjangoWhiteNoise
        application = DjangoWhiteNoise(application)
        ```

        これで、デプロイの準備完了！


その代わり、`mysite/settings.py`に以下を追加！(https://qiita.com/ymhr1121/items/344c4eb300ab9972d0c2)

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # この行を追加
    'django.contrib.sessions.middleware.SessionMiddleware',
# 以下略
]
```

### herokuにデプロイ

※ heroku toolbeltはインスコされている前提！

※もしCLIでherokuにログインしていな場合は、
```
$ heroku login
```
を実行！


```
$ heroku create [herokuアプリケーション名]
```


```
$ heroku run python manage.py migrate  -> migrateを実行!
$ heroku run python manage.py createsuperuser
```

デプロイ用では、

```
{
    username : adminuser
    email : admin@hoge.com
    password : hogehoge
}
```

で作成した！


### routing と viewsに関して

これは`^$`というパターンのURLをpost_listというビューに割り当てたことを意味します。

`^$` とは何を意味しているのでしょうか。それは正規表現のマジックです:）分解してみましょう：

正規表現での`^`は「文字列の開始」を意味します。ここからパターンマッチを始めます。

`$`は「文字列の終端」を意味していて、ここでパターンマッチを終わります。

この2つの記号を並べたパターンがマッチするのは、そう、空の文字列です。

といっても、DjangoのURL名前解決では 'http://127.0.0.1:8000/' は除いてパターンマッチするので、このパターンは 'http://127.0.0.1:8000/' 自体を意味します。

つまり、'http://127.0.0.1:8000/' というURLにアクセスしてきたユーザに対してviews.post_listを返すように指定していることになります。


### コンソール

```
$ python manage.py shell
```


```
>>> Post.objects.all()

Traceback (most recent call last): File "", line 1, in  NameError: name 'Post' is not defined
```
エラーになる！

これは、

```
>>> from blog.models import Post
```

```
>>> Post.objects.all()

<QuerySet [<Post: ロボットビジョンレポート>, <Post: j:opn>, <Post: ねsrb：っっktb>]>
```




