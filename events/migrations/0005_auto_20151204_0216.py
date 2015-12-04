# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventpicture_source_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpicture',
            name='source_albumname',
        ),
        migrations.RemoveField(
            model_name='eventpicture',
            name='source_username',
        ),
        migrations.AddField(
            model_name='eventpicture',
            name='source_albumlink',
            field=models.URLField(help_text=b'format: https://www.flickr.com/photos/77348536@N03/sets/72157660996201832/', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='eventpicture',
            name='source_projects',
            field=models.URLField(help_text=b'format: http://wearhacksla.devpost.com/submissions', max_length=100, blank=True),
        ),
    ]
