===
ngo
===

.. image:: https://travis-ci.org/naritotakizawa/ngo.svg?branch=master
    :target: https://travis-ci.org/naritotakizawa/ngo

.. image:: https://coveralls.io/repos/github/naritotakizawa/ngo/badge.svg?branch=master
    :target: https://coveralls.io/github/naritotakizawa/ngo?branch=master


DjangoライクなWebフレームワークです。

Requirement
===========
:Python: 3.4以上
 
 
Quick start
===========
1. pipでインストールする ::

    pip install -U https://github.com/naritotakizawa/ngo/archive/master.tar.gz


2. ngoプロジェクトの作成 ::

    ngo-admin startproject project


3. ngoアプリケーションの作成 ::

    python manage.py startapp app


4. project.settings.pyを編集 ::

    INSTALLED_APPS = [
        'app',
    ]


5. project.urls.pyを編集 ::

    from ngo.urls import url, include

    urlpatterns = [
        url(r'^', include('app.urls')),
    ]


6. 開発用サーバーを起動 ::

    python manage.py runserver

7. http://127.0.0.1:8000 へアクセス!
