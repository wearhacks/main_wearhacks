# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 2, 16, 54, 148432, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 2, 17, 10, 641790, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
