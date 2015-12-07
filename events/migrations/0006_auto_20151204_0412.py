# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20151204_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_albumlink', models.URLField(help_text=b'format: https://www.flickr.com/photos/77348536@N03/sets/72157660996201832/', max_length=100, blank=True)),
                ('source_type', models.CharField(max_length=1, choices=[(b'0', b'Other'), (b'1', b'flickr')])),
                ('source_projects', models.URLField(help_text=b'format: http://wearhacksla.devpost.com/submissions', max_length=100, blank=True)),
                ('participants', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.RemoveField(
            model_name='eventpicture',
            name='event',
        ),
        migrations.DeleteModel(
            name='EventPicture',
        ),
    ]
