# Generated by Django 2.0.2 on 2018-02-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_remove_song_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='genre',
            field=models.CharField(choices=[('Hollywood', 'Hollywood'), ('Rock', 'Rock'), ('Love', 'Love'), ('Hip-Hop', 'Hip-Hop'), ('Rap', 'Rap'), ('Metal', 'Metal'), ('Electrica', 'Electrica'), ('Bollywood', 'Bollywood'), ('Movie', 'Movie'), ('Dance', 'Dance'), ('Pop', 'Pop'), ('Soundtrack', 'Soundtrack'), ('Punjabi', 'Punjabi'), ('English', 'English'), ('Hindi', 'Hindi'), ('Remix', 'Remix'), ('Classical', 'Classical')], default='Bollywood', max_length=20),
        ),
    ]
