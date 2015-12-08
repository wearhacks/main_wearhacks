# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path, blank=True),
        ),
    ]
