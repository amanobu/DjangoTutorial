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
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]
