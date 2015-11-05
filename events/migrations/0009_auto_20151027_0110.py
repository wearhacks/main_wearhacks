# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20151021_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=150)),
                ('blog_post', models.URLField(max_length=100, blank=True)),
                ('submitted_event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.RemoveField(
            model_name='projects',
            name='submitted_event',
        ),
        migrations.DeleteModel(
            name='Projects',
        ),
    ]
