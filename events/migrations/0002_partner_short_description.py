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
            model_name='partner',
            name='short_description',
            field=models.CharField(default=datetime.datetime(2015, 11, 11, 3, 22, 46, 298334, tzinfo=utc), max_length=150),
            preserve_default=False,
        ),
    ]
