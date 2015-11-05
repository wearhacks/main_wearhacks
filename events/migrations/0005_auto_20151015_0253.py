# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20151013_0400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={'verbose_name_plural': 'Team Members'},
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(default=datetime.datetime(2015, 10, 15, 2, 53, 42, 442554, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='link',
            field=models.URLField(max_length=100, blank=True),
        ),
    ]
