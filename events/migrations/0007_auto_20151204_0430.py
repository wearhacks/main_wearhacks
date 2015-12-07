# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20151204_0412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pastevent',
            name='id',
        ),
        migrations.AlterField(
            model_name='pastevent',
            name='event',
            field=models.OneToOneField(primary_key=True, serialize=False, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='pastevent',
            name='participants',
            field=models.IntegerField(default=100),
        ),
    ]
