# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.http import Http404
from .models import Choice,Question
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

#「オブジェクトのリストを表示する」を抽象化
#Djangoには決まり切った処理の物が決まっているらしい：汎用View？と呼ばれいている様だ

class IndexView(generic.ListView):
    #ListViewは <app name>/<model name>_list.html というのをデフォルトで使うが、今回異なるので指示している
    template_name = 'polls/index.html'

    #いままではhtml側に値を渡すためにコンテキストに適当な変数を定義して渡していたが、DetailViewを使うと
    #modelに設定された内容で良さそうな名前でhtml側に渡す変数を定義されちゃう。
    #例えばDetailViewのClassはmodel = Questionなので question がそのままhtmlが側で拾えるらしい
    #ListViewだと、自動的に question_list となるが、今回html側ではすでに latest_question_list という変数で
    #値を取得しているので下記のコードでDjangoに使いたい変数名を指示している
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #この pub_date__lte=timezone.new() でpub_date が timezone.now 以前という条件指定が出来る様だ
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        #return Question.objects.order_by('-pub_date')[:5]

#「オブジェクトの詳細を表示する」を抽象化
class DetailView(generic.DetailView):
    #どのモデルの詳細を表示するかという指示に当たる模様
    model = Question
    #DetailViewは <app name>/<model name>_detail.html というのをデフォルトで使うが、今回異なるので指示している
    template_name = 'polls/detail.html'

    #汎用Viewでは'pk'という名前でURLからプライマリキーを持ってくることになっているので question_id を pk に変更している

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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

# 汎用Viewを使う事になったので未使用
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

# 汎用Viewを使う事になったので未使用
def detail(request, question_id):
    #get() を実行し、オブジェクトが存在しない場合には Http404 を送出することは非常によく使われるイディオムです。 Django はこのためのショートカットを提供しています
    #get_list_or_404() という関数もあります。この関数は get_object_or_404() と同じように動きますが、 get() ではなく、 filter() を使います。リストが空の場合は Http404 を送出します。
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# 汎用Viewを使う事になったので未使用
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


