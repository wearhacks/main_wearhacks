# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20151222_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventextend',
            name='extendKey',
            field=models.ForeignKey(help_text=b'Extension key', to='events.EventExtendType'),
        ),
    ]
