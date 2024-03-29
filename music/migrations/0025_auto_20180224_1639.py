# Generated by Django 2.0.2 on 2018-02-24 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0024_user_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='male', max_length=20)),
                ('date_of_birth', models.DateField(default='2000-10-10')),
                ('country', models.CharField(choices=[('India', 'India'), ('America', 'Ammerica')], default='India', max_length=20)),
                ('city', models.CharField(choices=[('Gurgaon', 'Gurgaon'), ('Delhi', 'Delhi')], default='Gurgaon', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='detail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
