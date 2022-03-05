# Generated by Django 3.2.9 on 2022-03-05 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('courses', '0022_course_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='content',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='course',
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='object_type',
            field=models.ForeignKey(default=1, limit_choices_to=models.Q(models.Q(('app_label', 'courses'), ('model', 'Course')), models.Q(('app_label', 'courses'), ('model', 'Content')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='contenttypes.contenttype'),
            preserve_default=False,
        ),
    ]