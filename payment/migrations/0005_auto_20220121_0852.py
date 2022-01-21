# Generated by Django 3.2.9 on 2022-01-21 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_courseenrollment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseenrollment',
            name='payment_method',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='online', max_length=20),
        ),
        migrations.AlterField(
            model_name='courseenrollment',
            name='payment_type',
            field=models.CharField(choices=[('telegram', 'Telegram'), ('fawry', 'Fawry'), ('visa', 'Visa'), ('free', 'Free')], default='free', max_length=20),
        ),
    ]