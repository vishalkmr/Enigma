# Generated by Django 2.0.2 on 2018-02-24 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0016_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=100)),
                ('date_of_birth', models.DateField()),
                ('country', models.CharField(choices=[('India', 'India'), ('America', 'America'), ('China', 'China'), ('South Africa', 'South Africa')], default='India', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
