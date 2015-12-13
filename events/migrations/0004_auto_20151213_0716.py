# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151213_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='first_link',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='second_link',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
