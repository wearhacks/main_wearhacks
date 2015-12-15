# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventcontent_eventpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcontent',
            name='html',
            field=models.TextField(max_length=500),
        ),
    ]
