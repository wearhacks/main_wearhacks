# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
    ]
