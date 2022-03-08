# Generated by Django 3.2.9 on 2022-03-08 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('playlists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='watchhistory',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watch_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='lecture',
            field=models.ManyToManyField(blank=True, to='courses.Lecture'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Playlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favorite',
            name='lecture',
            field=models.ManyToManyField(blank=True, to='courses.Lecture'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='playlist',
            unique_together={('owner', 'name')},
        ),
    ]
