# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_teammember_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='submitted_by',
        ),
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(null=True, upload_to=events.models.get_upload_path, blank=True),
        ),
        migrations.AddField(
            model_name='projects',
            name='submitted_event',
            field=models.ForeignKey(default='', to='events.Event'),
            preserve_default=False,
        ),
    ]
