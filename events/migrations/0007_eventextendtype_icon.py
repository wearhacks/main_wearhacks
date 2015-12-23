# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20151222_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventextendtype',
            name='icon',
            field=models.CharField(help_text=b'Icon for displaying on the front end (use fa icons).', max_length=b'50', null=True, blank=True),
        ),
    ]
