# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=150)),
                ('url', models.URLField(max_length=100, blank=True)),
                ('image', models.URLField(max_length=100, blank=True)),
                ('project_type', models.CharField(max_length=1, choices=[(b'0', b'staff'), (b'1', b'participant'), (b'2', b'winner')])),
                ('submitted_event', models.ForeignKey(to='events.Event', blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Project2'
        )

    ]
