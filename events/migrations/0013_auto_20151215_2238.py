# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20151215_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcontent',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.IntegerField(default=0, help_text=b'The order for the content to appear on the page.', validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
