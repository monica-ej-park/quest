from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from datetime import date
from django.db.models import F, Sum, Count, Case, When


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
        for record in records:
            record.category = Action.category_type_choices[record.category][1]
        return records


    def query_total_xp(self, user):
        return Record.objects.filter(
            user=user,
        ).aggregate(Sum('xp'))['xp__sum'] 
        

    def query_xp_per_action(self, user, days):
        records = Record.objects.filter(
            user=user, 
            date__range=[date.today() - datetime.timedelta(days=6), 
            date.today()]
        ).values(
            'action'
        ).annotate(
            category=F('action__category'),
            name=F('action__name'),
            total_xp=Sum('xp'),
            total_repeat=Sum('repeat'),
        )
        for record in records:
            record['category'] = Action.category_type_choices[record['category']][1]
        return records
        

    def query_xp_per_day(self, user, days):
        return Record.objects.filter(
            user=user, 
            date__range=[date.today() - datetime.timedelta(days=6), 
            date.today()]
        ).values(
            'date'
        ).annotate(
            daily_total_xp=Sum('xp')
        ).order_by(
            '-date'
        )
    


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=False)
    memo = models.CharField(max_length=10, default="", blank=True, verbose_name="추가설명")
    repeat = models.IntegerField(default=1, verbose_name="반복 횟수")
    xp = models.IntegerField(default=0, verbose_name="경험치")
    date = models.DateField(verbose_name="날짜", default=datetime.date.today, auto_created=True)
    time = models.TimeField(verbose_name="시간", default=timezone.now, auto_created=True)

    objects = RecordManager()





