# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151218_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastEvent',
            fields=[
                ('source_albumlink', models.URLField(help_text=b'format: https://www.flickr.com/photos/77348536@N03/sets/72157660996201832/', max_length=100, blank=True)),
                ('source_type', models.CharField(max_length=1, choices=[(b'0', b'Other'), (b'1', b'flickr')])),
                ('source_projects', models.URLField(help_text=b'format: http://wearhacksla.devpost.com/submissions', max_length=100, blank=True)),
                ('participants', models.IntegerField(default=100)),
                ('event', models.OneToOneField(primary_key=True, serialize=False, to='events.Event')),
            ],
        ),
    ]
