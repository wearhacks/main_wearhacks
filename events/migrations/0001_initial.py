# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import events.models.helpers


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
                ('photo', models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path_event, blank=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('link', models.URLField(max_length=100, blank=True)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),

        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('partner_type', models.CharField(max_length=1, choices=[(b'0', b'Global Partners'), (b'1', b'Hardware Partners'), (b'2', b'Media Partners'), (b'3', b'Membership')])),
                ('photo', models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path, blank=True)),
                ('link', models.URLField(max_length=100, blank=True)),
                ('short_description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=300)),
                ('url', models.URLField(max_length=500, blank=True)),
                ('image', models.URLField(max_length=500, blank=True)),
                ('project_type', models.CharField(max_length=1, choices=[(b'0', b'staff'), (b'1', b'participant'), (b'2', b'winner')])),
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
                ('photo', models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path, blank=True)),
                ('github', models.URLField(max_length=100, blank=True)),
                ('linkedin', models.URLField(max_length=100, blank=True)),
                ('facebook', models.URLField(max_length=100, blank=True)),
                ('twitter', models.URLField(max_length=100, blank=True)),
                ('order', models.DecimalField(default=0, max_digits=100, decimal_places=0)),
            ],
        ),
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
        migrations.AddField(
            model_name='project',
            name='submitted_event',
            field=models.ForeignKey(to='events.Event', blank=True),
        ),
    ]
