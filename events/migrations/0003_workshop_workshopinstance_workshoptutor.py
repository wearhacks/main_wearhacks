# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151213_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('short_description', models.CharField(max_length=150)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path, validators=[events.models.helpers.validate_large_image])),
                ('difficulty', models.CharField(max_length=1, choices=[(b'0', b'Beginner'), (b'1', b'Intermediate'), (b'2', b'Advanced')])),
                ('required_tools', models.CharField(max_length=150)),
                ('technologies', models.CharField(help_text=b'Software or hardware technologies thought in this workshop', max_length=150)),
                ('duration', models.CharField(help_text=b'Approximate duration of the course', max_length=150)),
                ('schedule', models.TextField(default=b'<ul><li><span>9:00AM</span> Quick Introduction</li><li><span>-:--AM</span> etc </li></ul>')),
                ('workshop_outline', models.TextField(default=b'<h1>What is this workshop about?</h1> <p>Describe event<p>')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(blank=True)),
                ('end_date', models.DateTimeField(blank=True)),
                ('eventbrite_link', models.URLField()),
                ('slug', models.SlugField(help_text=b'ie: Short name, required field for event page: http://wearhacks.com/workshops/<slug>')),
                ('address', models.CharField(max_length=100)),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('parent_workshop', models.ForeignKey(to='events.Workshop', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopTutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, verbose_name=b'email')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path, validators=[events.models.helpers.validate_small_image])),
                ('background', models.TextField(max_length=150)),
                ('workshop', models.ForeignKey(to='events.WorkshopInstance', blank=True)),
            ],
        ),
    ]
