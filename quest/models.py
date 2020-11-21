from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from datetime import date
from django.db.models import F, Sum, Count, Case, When, Subquery, Value
from django.db.models.functions import Concat

class Action(models.Model):
    category_type_choices = (
        (0, '공부'),
        (1, '문화/예술'),
        (2, '운동'),
        (3, '자기관리'),
        (4, '집안일'),
        (5, '게임'),
        (6, '유투브'),
        (7, '인터넷'),
        (8, '기타'),
        (9, '수업'),
        (10, '퀘스트'),
    )
    category = models.IntegerField(default=0, choices=category_type_choices, verbose_name="카테고리")
    name = models.CharField(null=False, max_length=100, verbose_name="행동이름")
    xp = models.IntegerField(default=0, verbose_name="경험치")


    def __str__(self):
        return f'{self.category_type_choices[self.category][1]}  |  {self.name}  |  {self.xp}'


class RecordManager(models.Manager):
    def query_all(self, user):
        records = Record.objects.filter(
            user=user, date=date.today()
        ).annotate(
            category=F('action__category')
        ).order_by('-id')
#        for record in records:
#            record.category = Action.category_type_choices[record.category][1]
        return records


    # 누적 총 xp
    def query_total_xp(self, user):
        return Record.objects.filter(
            user=user,
            checked=True
        ).aggregate(Sum('xp'))['xp__sum'] 

    # 미확인 xp (게임제외)
    def query_unchecked_xp(self, user):
        return Record.objects.filter(
            user=user,
            checked=False
        ).exclude(
            action__category=5
        ).aggregate(Sum('xp'))['xp__sum']    

    # 미확인 게임 xp (삭감 예정)
    def query_unchecked_spent_xp(self, user):
        return Record.objects.filter(
            user=user,
            checked=False,
            action__category=5
        ).aggregate(Sum('xp'))['xp__sum']   


    # 기간내 액션별 총 xp
    def query_xp_per_action(self, user, days):
        records = Record.objects.filter(
            user=user, 
            date__range=[date.today() - datetime.timedelta(days=days), date.today()],
            checked=True
        ).values(
            'action'#, 'action__category'
        ).annotate(
            category=F('action__category'),
            name=F('action__name'),
            total_xp=Sum('xp'),
            total_repeat=Sum('repeat'),
        )
        for record in records:
            record['category'] = Action.category_type_choices[record['category']][1]
        return records
        

    # 기간별 총 xp
    def query_xp_per_day(self, user, days):
        return Record.objects.filter(
            user=user, 
            date__range=[date.today() - datetime.timedelta(days=days), date.today()],
            checked=True
        ).exclude(
            action__category=5
        ).values(
            'date'
        ).annotate(
            daily_earned_xp=Sum('xp')
        )
        

    # 기간별 게임에 소비한 xp
    def query_xp_for_game(self, user, days):
        return Record.objects.filter(
            user=user,
            action__category=5, # 게임 == 5
            date__range=[date.today() - datetime.timedelta(days=days), date.today()],
            checked=True
        ).values(
            'date'
        ).annotate(
            daily_spent_xp=Sum('xp')
        )#.order_by(
        #    '-date'
        #)



class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=False)
    memo = models.CharField(max_length=60, default="", blank=True, verbose_name="추가설명")
    repeat = models.IntegerField(default=1, verbose_name="반복 횟수")
    xp = models.IntegerField(default=0, verbose_name="경험치")
    date = models.DateField(verbose_name="날짜", default=datetime.date.today, auto_created=True)
    time = models.TimeField(verbose_name="시간", default=timezone.now, auto_created=True)
    checked = models.BooleanField(verbose_name="확인", default=False)

    objects = RecordManager()

"""
경험치 펜딩/수락 상태 표시 필드 추가하기

"""




class Quest(models.Model):
    category_type_choices = (
        (0, '공부'),
        (1, '문화/예술'),
        (2, '운동'),
        (3, '자기관리'),
        (4, '집안일'),
        (5, '게임'),
        (6, '유투브'),
        (7, '인터넷'),
        (8, '기타'),
        (9, '수업'),
        (10, '퀘스트'),
    )
    category = models.IntegerField(default=0, choices=category_type_choices, verbose_name="카테고리")
    name = models.CharField(null=False, max_length=100, verbose_name="퀘스트 이름")
    desc = models.TextField(null=True, verbose_name="퀘스트 내용")
    xp = models.IntegerField(default=0, verbose_name="경험치")    
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name="수행자")
    accomplishment = models.BooleanField(default=False, verbose_name="수행 여부")
