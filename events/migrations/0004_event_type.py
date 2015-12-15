# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151214_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(default=b'hackathon', max_length=1, choices=[(b'workshop', b'Workshop'), (b'alpha_hack', b'Alpha Hack'), (b'hackathon', b'Hackathon')]),
        ),
    ]
