# Generated by Django 3.2.9 on 2022-03-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseactivity',
            name='left_off_at',
            field=models.PositiveIntegerField(default=0),
        ),
    ]