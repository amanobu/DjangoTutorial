# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
# 管理ページにPollアプリを認識させ編集出来るようにする
from .models import Question,Choice

#Questionの追加時に連動して3つ分Choiceも追加する
#TabularInline というのもある
class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3

#管理ツールでQuestionの表示オプションを変更する
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields':['question_text']}),
        ('Date infomation',{'fields':['pub_date'], 'classes': ['collapse']}),
        ]
    inlines = [ChoiceInLine]
    
    #管理画面で表示される項目.勝手にDjangoが訂正する。(この表記を変えたいときはmodels.pyを修正する)
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    #管理画面で指定した項目の絞り込みメニューがでる
    list_filter = ['pub_date']

    #これで検索出来る様になる
    search_fields = ['question_text']

#このように2引数に渡すとオプションを変更出来るそうだ
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Question)
#admin.site.register(Choice)
