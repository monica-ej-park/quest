# Generated by Django 3.1.3 on 2020-11-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0006_record_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='repeat',
            field=models.IntegerField(default=1, verbose_name='반복 횟수'),
        ),
    ]