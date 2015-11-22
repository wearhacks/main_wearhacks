# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='blog_post',
            new_name='image',
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.CharField(default=' ', max_length=1, choices=[(b'0', b'staff'), (b'1', b'participant'), (b'2', b'winner')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='url',
            field=models.URLField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='submitted_event',
            field=models.ForeignKey(to='events.Event', blank=True),
        ),
    ]
