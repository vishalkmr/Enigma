# Generated by Django 2.0.2 on 2018-02-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0032_auto_20180225_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='duration',
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default='1111-11-11'),
        ),
    ]
