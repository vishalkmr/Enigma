# Generated by Django 2.0.2 on 2018-02-22 13:33

from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_song_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='file_type',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='album',
            name='pub_year',
            field=models.IntegerField(default=2018, validators=[music.models.validate_year]),
        ),
        migrations.AlterField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[('Bollywood', 'Bollywood'), ('Country', 'Country'), ('Classical', 'Classical'), ('Dance', 'Dance'), ('Electrica', 'Electrica'), ('English', 'English'), ('Hindi', 'Hindi'), ('Hip-Hop', 'Hip-Hop'), ('Hollywood', 'Hollywood'), ('Love', 'Love'), ('Metal', 'Metal'), ('Movie', 'Movie'), ('Pop', 'Pop'), ('Punjabi', 'Punjabi'), ('Rap', 'Rap'), ('Remix', 'Remix'), ('Rock', 'Rock'), ('Soundtrack', 'Soundtrack'), ('Unkonwn', 'Unkonwn')], default='Bollywood', max_length=20),
        ),
    ]
