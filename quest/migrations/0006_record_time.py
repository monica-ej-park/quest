# Generated by Django 3.1.3 on 2020-11-12 06:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0005_auto_20201112_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.TimeField(auto_created=True, default=django.utils.timezone.now, verbose_name='시간'),
        ),
    ]