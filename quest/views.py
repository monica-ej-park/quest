from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RecordForm
from .models import Record, Action
from datetime import date
import datetime
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
        records = Record.objects.filter(user=user).order_by('-id')
        total_xp = 0
        for r in records:
            r.action.category = r.action.category_type_choices[r.action.category][1]
            total_xp += r.xp

        actions = Action.objects.all()    
        if term == 'today':
            records = Record.objects.filter(user=user, date=date.today()).order_by('-id')
            field_names = ["카테고리", "행동", "반복횟수", "경험치", '메모', '날짜', '시간']

        elif term == 'week':
            records = Record.objects.filter(user=user, date__range=[date.today() - datetime.timedelta(days=6), date.today()]).order_by('-id')

            # 일별 경험치 합
            #for r in records:

            # 액션별 경험치 합    
            for a, i in zip(actions, range(0, len(actions))):
                a.repeat = 0
                a.xp = 0
                a.category = a.category_type_choices[a.category][1]
                for r in records:
                    if a.name == r.action.name:
                        a.repeat += r.repeat
                        a.xp += r.xp
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
            records = actions
                
        elif term == 'month':
            records = Record.objects.filter(user=user, date__range=[date.today() - datetime.timedelta(days=29), date.today()]).order_by('-id')
            
            # 일별 경험치 합
            #for r in records:

            # 액션별 경험치 합             
            for a, i in zip(actions, range(0, len(actions))):
                a.repeat = 0
                a.xp = 0
                a.category = a.category_type_choices[a.category][1]
                for r in records:
                    if a.name == r.action.name:
                        a.repeat += r.repeat
                        a.xp += r.xp
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
            records = actions
        else:          
            term = 'total'
            # 일별 경험치 합
            #for r in records:

            # 액션별 경험치 합 
            for a, i in zip(actions, range(0, len(actions))):
                a.repeat = 0
                a.xp = 0
                a.category = a.category_type_choices[a.category][1]
                for r in records:
                    if a.name == r.action.name:
                        a.repeat += r.repeat
                        a.xp += r.xp
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
            records = actions


        form = RecordForm()
        form.fields['user'].initial = user


        return render(
            request, 
            'quest/record.html', 
            {
                'page_name': 'record',
                'username': username,
                'total_xp': total_xp, 
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
                'xp_per_day': []               
            }
        )


def record_kjy(request, username):
    return record(request=request, username=username, term='today')

def record_kjh(request, username):
    return record(request=request, username=username, term='today')


def record_today(request):
    pass

def show_xpsheets(request):
    data_list = Action.objects.all()
    for data in data_list:
        data.category = data.category_type_choices[data.category][1]
    
    return render(
        request, 
        'quest/record.html', 
        {"page_name": 'xpsheets', 'data_list': data_list, 'field_names': ["카테고리", "행동", "경험치"]}
    )