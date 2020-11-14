from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Action(models.Model):
    category_type_choices = (
        (0, '공부'),
        (1, '문화/예술'),
        (2, '운동'),
        (3, '자기관리'),
        (4, '집안일'),
    )
    category = models.IntegerField(default=0, choices=category_type_choices, verbose_name="카테고리")
    name = models.CharField(null=False, max_length=100, verbose_name="행동이름")
    xp = models.IntegerField(default=0, verbose_name="경험치")


    def __str__(self):
        return f'{self.category_type_choices[self.category][1]}  |  {self.name}  |  {self.xp}'


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=False)
    memo = models.CharField(max_length=10, default="", blank=True, verbose_name="추가설명")
    repeat = models.IntegerField(default=1, verbose_name="반복 횟수")
    xp = models.IntegerField(default=0, verbose_name="경험치")
    date = models.DateField(verbose_name="날짜", default=datetime.date.today, auto_created=True)
    time = models.TimeField(verbose_name="시간", default=timezone.now, auto_created=True)



