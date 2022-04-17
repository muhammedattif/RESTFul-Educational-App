# Generated by Django 3.2.9 on 2022-04-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_analytics', '0002_rename_model_aggregatecard_model_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100)),
                ('operator', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='aggregatecard',
            name='aggregate_field',
            field=models.CharField(blank=True, default='pk', max_length=100),
        ),
    ]
