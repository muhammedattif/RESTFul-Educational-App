# Generated by Django 3.2.9 on 2021-11-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211123_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='academic_year',
            field=models.IntegerField(blank=True, choices=[(1, 'FIRST'), (2, 'SECOND'), (3, 'THIRD'), (4, 'FOURTH'), (5, 'FIFTH'), (6, 'SIXTH'), (7, 'SEVENTH')]),
        ),
    ]
