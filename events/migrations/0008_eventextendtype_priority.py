# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventextendtype_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventextendtype',
            name='priority',
            field=models.IntegerField(default=1, help_text=b'The order for the extension to appear on the page.', validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
