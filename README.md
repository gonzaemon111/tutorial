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