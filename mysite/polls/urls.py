# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'polls'

urlpatterns = [
    # 1:regrex:マッチするURLのパターン
    # 2:view:マッチしたURLパターンがあったら所定のビュー関数を呼び出す
    # 3:kwargs:余り使わないがURL
    # 4:name:名前を設定しておくと、Djangoの度々からでも明確に参照出来る
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]
