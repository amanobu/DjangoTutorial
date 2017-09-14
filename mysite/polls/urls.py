# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
app_name = 'polls'

urlpatterns = [
    # 1:regrex:マッチするURLのパターン
    # 2:view:マッチしたURLパターンがあったら所定のビュー関数を呼び出す
    # 3:kwargs:余り使わないがURL
    # 4:name:名前を設定しておくと、Djangoの度々からでも明確に参照出来る
    # ex: /polls/
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', login_required(views.ResultView.as_view()), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', login_required(views.vote), name='vote'),
    #login
    url(r'^login$', auth_views.login,  { 'template_name': 'polls/login.html' }, name='login'),
    #url('^', include('django.contrib.auth.urls')),
    ]
