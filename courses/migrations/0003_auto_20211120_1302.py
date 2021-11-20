# Generated by Django 3.2.9 on 2021-11-20 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachement',
            name='course',
        ),
        migrations.CreateModel(
            name='ContentAttachement',
            fields=[
                ('attachement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.attachement')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='courses.content')),
            ],
            bases=('courses.attachement',),
        ),
        migrations.CreateModel(
            name='CourseAttachement',
            fields=[
                ('attachement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.attachement')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='courses.course')),
            ],
            bases=('courses.attachement',),
        ),
    ]