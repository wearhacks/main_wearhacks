# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151129_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpicture',
            name='source_projects',
            field=models.URLField(max_length=100, blank=True),
        ),
    ]
