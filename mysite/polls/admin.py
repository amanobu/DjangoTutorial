# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
# 管理ページにPollアプリを認識させ編集出来るようにする
from .models import Question

admin.site.register(Question)
