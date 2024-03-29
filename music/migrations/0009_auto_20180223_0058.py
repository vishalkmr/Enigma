# Generated by Django 2.0.2 on 2018-02-22 19:28

from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20180222_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(upload_to='music/static/media/album_logo/', validators=[music.models.validate_image]),
        ),
    ]
