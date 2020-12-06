from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RecordForm, QuestForm
from .models import Record, Action, Quest
from datetime import date
import datetime
from django.db.models import F, Sum, Count, Case, When
# Create your views here.

def record(request, username, term):
    user = User.objects.get(username=username)
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():         
            form.save()
            return redirect("record", username, term)

        else:
            print(form.errors)
  
    else:
        records = None        
        field_names = None
        earned_xp = []
        spent_xp = []
        dates = []
        graph_data = []
        days = 0
 
        actions = Action.objects.all()    
        if term == 'today':
            records = Record.objects.query_all(user=user)
            field_names = ["카테고리", "행동", "반복횟수", "경험치", '날짜', '시간', '확인']
        elif term == 'week':
            days = 6
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]           
        elif term == 'month':
            days = 29
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
        else:          
            term = 'total'
            days = 364
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]

        if term != 'today':    
            records = Record.objects.query_xp_per_action(user=user, days=days)
            earned_xp = Record.objects.query_xp_per_day(user=user, days=days)
            spent_xp = Record.objects.query_xp_for_game(user=user, days=days)


        form = RecordForm()
        form.fields['user'].initial = user

        return render(
            request, 
            'quest/record.html', 
            {
                'page_name': 'record',
                'username': username,
                'total_xp': Record.objects.query_total_xp(user=user), # 누적 총 xp
                'unchecked_xp': Record.objects.query_unchecked_xp(user=user),
                'unchecked_spent_xp': Record.objects.query_unchecked_spent_xp(user=user),
                'form': form, 
                'data_list': records,
                'field_names': field_names,
                'record_tabs': [
                    {'id':'today', 'name':"오늘"}, 
                    {'id':'week', 'name': "일주일"}, 
                    {'id': 'month', 'name': "한달"}, 
                    {'id':'total', 'name': "전체"}
                ],
                'selected_tab': term,
                'earned_xp': earned_xp,  # 기간별 벌어들인 xp # 기간별 소비한 xp   
                'spent_xp': spent_xp        
            }
        )


def record_kjy(request, username):
    return record(request=request, username=username, term='today')

def record_kjh(request, username):
    return record(request=request, username=username, term='today')


def show_xpsheets(request):
    data_list = Action.objects.all()

    return render(
        request, 
        'quest/xpsheets.html', 
        {"page_name": 'xpsheets', 'data_list': data_list, 'field_names': ["카테고리", "행동", "경험치"]}
    )


def quests(request):
    data_list = Quest.objects.all()#filter(accomplishment=False)
    return render(
        request, 
        'quest/quest.html', 
        {
            "page_name": 'quests', 
            'data_list': data_list, 
            'field_names': ["카테고리", "퀘스트", "수행자", ""]
        }
    )

def quests_accomplish(request, data_id):
    q = Quest.objects.get(id=data_id)
    q.accomplishment = True
    q.save()
    #Record.objects.create(user=q.to, action=q.)
    return quests(request)


def check(request):
    records = Record.objects.filter(checked=False)
    return render(
        request, 
        'quest/check.html', 
        {
            "page_name": 'check', 
            'data_list': records, 
            'field_names': ["수행자", "행동", "반복횟수", "경험치", "모두선택"]
        }
    )