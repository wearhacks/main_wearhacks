# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20151215_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(help_text=b'ie: Short name, required field for event page: http://wearhacks.com/events/<slug>'),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(default=b'hackathon', max_length=10, choices=[(b'workshop', b'Workshop'), (b'alpha_hack', b'Alpha Hack'), (b'hackathon', b'Hackathon')]),
        ),
        migrations.AlterField(
            model_name='eventpicture',
            name='photo',
            field=models.ImageField(upload_to=events.models.helpers.get_upload_path_event_picture),
        ),
    ]
