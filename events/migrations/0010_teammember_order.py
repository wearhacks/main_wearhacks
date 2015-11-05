# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20151027_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='order',
            field=models.DecimalField(default=0, max_digits=100, decimal_places=0),
        ),
    ]
