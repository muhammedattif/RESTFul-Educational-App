# Generated by Django 3.2.9 on 2022-01-21 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_alter_courseactivity_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='duration',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
