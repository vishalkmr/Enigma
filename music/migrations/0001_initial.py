# Generated by Django 2.0.2 on 2018-02-21 15:30

from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_title', models.CharField(max_length=500)),
                ('album_logo', models.FileField(upload_to='media/album_logo/', validators=[music.models.validate_image])),
                ('pub_year', models.IntegerField(validators=[music.models.validate_year])),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=250)),
                ('artist', models.CharField(max_length=250)),
                ('audio_file', models.FileField(upload_to='media/songs/')),
                ('genre', models.CharField(max_length=100)),
                ('duration', models.DurationField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
            ],
        ),
    ]
