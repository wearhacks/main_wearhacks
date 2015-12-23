# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_eventextendtype_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventextendtype',
            name='format',
            field=models.CharField(help_text=b'Text to add around the value. Use [v] to indicate where the value should be added.', max_length=b'50', null=True, blank=True),
        ),
    ]
