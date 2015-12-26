# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
            name='EventExtend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(help_text=b'Extension value')),
            ],
        ),
        migrations.CreateModel(
            name='EventExtendType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'Keyword to name this extension.', max_length=b'50')),
                ('description', models.CharField(help_text=b'Short description of what this extensions is about.', max_length=b'250')),
                ('values', models.CharField(help_text=b'Allowed values (for list, delimetered by comma.', max_length=b'250', null=True, blank=True)),
                ('icon', models.CharField(help_text=b'Icon for displaying on the front end (use fa icons).', max_length=b'50', null=True, blank=True)),
                ('priority', models.IntegerField(help_text=b'The order for the extension to appear on the page.', validators=[django.core.validators.MinValueValidator(0)])),
                ('format', models.CharField(help_text=b'Text to add around the value. Use [v] to indicate where the value should be added.', max_length=b'50', null=True, blank=True)),
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
            name='ExtendType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(help_text=b'Give a name to your custom type.', max_length=b'50')),
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
            model_name='eventextendtype',
            name='type',
            field=models.ForeignKey(to='events.ExtendType'),
        ),
        migrations.AddField(
            model_name='eventextend',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='eventextend',
            name='extendKey',
            field=models.ForeignKey(help_text=b'Extension key', to='events.EventExtendType'),
        ),
        migrations.AddField(
            model_name='eventcontent',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
    ]
