# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20151215_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcontent',
            name='html',
            field=tinymce.models.HTMLField(),
        ),
    ]
