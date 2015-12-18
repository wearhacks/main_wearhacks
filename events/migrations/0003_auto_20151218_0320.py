# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.models.helpers
import tinymce.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151213_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(help_text=b'The order for the content to appear on the page.', validators=[django.core.validators.MinValueValidator(0)])),
                ('size', models.CharField(default=b'large-12', help_text=b'Fondation column class for responsiveness.', max_length=b'50', choices=[(b'large-12', b'Full Width'), (b'large-6 medium-12', b'Large Half Width'), (b'medium-6 small-12', b'Large and Medium Half Width'), (b'large-4 medium-6 small-12', b'Third Width'), (b'large-3 medium-4 small-6', b'Forth Width')])),
                ('html', tinymce.models.HTMLField()),
                ('draft', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EventPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=events.models.helpers.get_upload_path_event_picture)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField(help_text=b'Number of tickets available. -1 for infinite.', validators=[django.core.validators.MinValueValidator(-1)])),
                ('priority', models.IntegerField(help_text=b'The order for the content to appear on the page.', validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(default=b'hackathon', max_length=10, choices=[(b'workshop', b'Workshop'), (b'alpha_hack', b'Alpha Hack'), (b'hackathon', b'Hackathon')]),
        ),
        migrations.AddField(
            model_name='event',
            name='registration_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='eventpicture',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='eventcontent',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
    ]
