# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20151215_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registration',
            name='ticket',
            field=models.ForeignKey(default=False, to='events.Ticket'),
            preserve_default=False,
        ),
    ]
