# Generated by Django 5.2 on 2025-05-18 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_playlist_songs'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='song_images/'),
        ),
    ]
