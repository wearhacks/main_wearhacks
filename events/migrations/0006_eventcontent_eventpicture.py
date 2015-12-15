# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20151214_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.CharField(max_length=225)),
                ('priority', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('size', models.CharField(default=b'large-12', max_length=b'50', choices=[(b'large-12', b'Full Width'), (b'large-6 medium-12', b'Large Half Width'), (b'medium-6 small-12', b'Large and Medium Half Width'), (b'large-4 medium-6 small-12', b'Third Width'), (b'large-3 medium-4 small-6', b'Forth Width')])),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=events.models.helpers.get_upload_path_event)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
    ]
