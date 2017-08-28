# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
#これから開発する簡単な poll アプリケーションでは、投票項目 (Question) と選択肢 (Choice) の二つのモデルを作成します。
#Poll には質問事項 (question) と公開日 (publication date) の情報があります。
#Choice には選択肢のテキストと投票数 (vote) という二つのフィールドがあります。各 Choice は一つの Question に関連づけられています

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    #表示での利便性のためだけではなく、、Djangoの自動生成adminでオブジェクトの表現として使用されるという理由からも __str__() メソッドをモデルに追加することは重要
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    #Question classと同じ意味で追加
    def __str__(self):
        return self.choice_text

    
