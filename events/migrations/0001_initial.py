# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import events.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField(blank=True)),
                ('end_date', models.DateTimeField(blank=True)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('photo', models.ImageField(null=True, upload_to=events.models.get_upload_path_event, blank=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('link', models.URLField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('partner_type', models.CharField(max_length=1, choices=[(b'0', b'Global Partners'), (b'1', b'Hardware Partners'), (b'2', b'Media Partners'), (b'3', b'Membership')])),
                ('photo', models.ImageField(null=True, upload_to=events.models.get_upload_path, blank=True)),
                ('link', models.URLField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=150)),
                ('blog_post', models.URLField(max_length=100, blank=True)),
                ('submitted_event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('blurb', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, verbose_name=b'email')),
                ('photo', models.ImageField(null=True, upload_to=events.models.get_upload_path, blank=True)),
                ('github', models.URLField(max_length=100, blank=True)),
                ('linkedin', models.URLField(max_length=100, blank=True)),
                ('facebook', models.URLField(max_length=100, blank=True)),
                ('twitter', models.URLField(max_length=100, blank=True)),
                ('order', models.DecimalField(default=0, max_digits=100, decimal_places=0)),
            ],
            options={
                'verbose_name_plural': 'Team Members',
            },
        ),
    ]
