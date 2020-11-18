from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RecordForm
from .models import Record, Action
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
        xp_per_day = []
        
        total_xp = Record.objects.query_total_xp(user=user)
 
        actions = Action.objects.all()    
        if term == 'today':
            #records = Record.objects.filter(user=user, date=date.today()).order_by('-id')
            records = Record.objects.query_all(user=user)
            #for record in records:
            #    print(record['category'])
                #record['category'] = Action.category_type_choices[record['category']][1]

            field_names = ["카테고리", "행동", "반복횟수", "경험치", '메모', '날짜', '시간']
        elif term == 'week':
            records = Record.objects.query_xp_per_action(user=user, days=6)
            xp_per_day = Record.objects.query_xp_per_day(user=user, days=6)
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
        elif term == 'month':
            records = Record.objects.query_xp_per_action(user=user, days=29)
            xp_per_day = Record.objects.query_xp_per_day(user=user, days=29)
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
        else:          
            term = 'total'
            records = Record.objects.query_xp_per_action(user=user, days=364)
            xp_per_day = Record.objects.query_xp_per_day(user=user, days=364)
            field_names = ["카테고리", "행동", "반복횟수", "경험치"]
            

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
                'xp_per_day': xp_per_day               
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


def quest(request):
    pass