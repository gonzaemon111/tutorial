# これはDjangoのメソッドと、blogアプリの全てのビュー（といっても、今は一つもありません。すぐに作りますけど！）をインポートするという意味です。
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]