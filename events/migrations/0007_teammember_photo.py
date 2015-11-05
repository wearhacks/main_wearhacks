# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20151015_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='photo',
            field=models.ImageField(null=True, upload_to=events.models.get_upload_path, blank=True),
        ),
    ]
