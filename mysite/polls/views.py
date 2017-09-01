# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.http import Http404
from .models import Choice,Question
from django.db.models import F
# Create your views here.

#def index(request):
#    #システム上にある最新の 5 件
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    #テンプレートの読み込み
#    template = loader.get_template('polls/index.html')
#    #コンテキストは、テンプレート変数名を Python オブジェクトへのマッピングしている辞書です。
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    #output = ', '.join([q.question_text for q in latest_question_list])
#    #return HttpResponse(output)
#    return HttpResponse(template.render(context,request))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    #テンプレートをロードしてコンテキストに値を入れ、テンプレートをレンダリングした結果を HttpResponse オブジェクトで返す、というイディオムは非常によく使われます。 Django はこのためのショートカットを提供します
    return render(request, 'polls/index.html', context)


# ＵＲＬの追加分
#def detail(request, question_id):
#    #return HttpResponse("You're looking at question %s." % question_id)
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist!!!")
#    return render(request, 'polls/detail.html', {'question': question})


def detail(request, question_id):
    #get() を実行し、オブジェクトが存在しない場合には Http404 を送出することは非常によく使われるイディオムです。 Django はこのためのショートカットを提供しています
    #get_list_or_404() という関数もあります。この関数は get_object_or_404() と同じように動きますが、 get() ではなく、 filter() を使います。リストが空の場合は Http404 を送出します。
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    #response =  "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)

    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #request.POST の値は常に文字列
        #POST データに choice がなければ、 request.POST['choice'] は KeyError を送出します
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did't select a choice",
            })
    else:
        #カウンタの追加
        #selected_choice.votes += 1
        #↑だと複数要求による更新でこのままだと不正なアップデートがあり得る(LOCKしてないから)
        #それを防ぐための解決方法が：https://docs.djangoproject.com/ja/1.10/ref/models/expressions/#avoiding-race-conditions-using-f
        #その場合以下の様に書くと良いらしい
        selected_choice.votes = F('votes') + 1 #selected_choice.votes += 1の替わり
        selected_choice.save()
        #POSTに成功したときは、常にHttpResponseRedirectを戻すべきだそうだ
        #ブラウザの戻るボタンとか押したときに2度POST送信される事を防ぐため
        #reverse()はビュー関数中での URL のハードコードを防げます。関数には、制御を渡したいビューの名前と、そのビューに与える URL パターンの位置引数を与えます。すると'/polls/question.id/results/'という文字列が返ってくる
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


