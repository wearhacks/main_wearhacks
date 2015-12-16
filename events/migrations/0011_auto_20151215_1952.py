# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_slider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='type',
            new_name='event_type',
        ),
    ]
