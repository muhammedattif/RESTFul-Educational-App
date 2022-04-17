# Generated by Django 3.2.9 on 2022-04-15 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('aggrigate_function', models.CharField(choices=[('count', 'Count'), ('sum', 'Sum'), ('min', 'Min'), ('max', 'Max'), ('average', 'Average')], max_length=100)),
                ('conditions', models.TextField(blank=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
