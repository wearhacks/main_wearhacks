# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20151215_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='stock',
            field=models.IntegerField(default=10, help_text=b'Number of tickets available. -1 for infinite.', validators=[django.core.validators.MinValueValidator(-1)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventcontent',
            name='priority',
            field=models.IntegerField(help_text=b'The order for the content to appear on the page.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='eventcontent',
            name='size',
            field=models.CharField(default=b'large-12', help_text=b'Fondation column class for responsiveness.', max_length=b'50', choices=[(b'large-12', b'Full Width'), (b'large-6 medium-12', b'Large Half Width'), (b'medium-6 small-12', b'Large and Medium Half Width'), (b'large-4 medium-6 small-12', b'Third Width'), (b'large-3 medium-4 small-6', b'Forth Width')]),
        ),
    ]
