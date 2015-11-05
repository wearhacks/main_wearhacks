# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151008_0217'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('blurb', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, verbose_name=b'email')),
                ('github', models.URLField(max_length=100, blank=True)),
                ('linkedin', models.URLField(max_length=100, blank=True)),
                ('facebook', models.URLField(max_length=100, blank=True)),
                ('twitter', models.URLField(max_length=100, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='short_name',
            field=models.CharField(default=datetime.datetime(2015, 10, 13, 3, 27, 33, 833079, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
