# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models.registration
import re
import events.models.helpers
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151213_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('charge_id', models.CharField(max_length=27)),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hacker', models.CharField(default=b'Unknown', max_length=200)),
                ('is_livemode', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_captured', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'No Status', max_length=100)),
                ('source_id', models.CharField(max_length=29)),
                ('failure_message', models.CharField(default=b'No Error', help_text=b'Charge object failure message', max_length=200, blank=True)),
                ('failure_code', models.CharField(default=b'200', help_text=b'Charge object failure code', max_length=200, blank=True)),
                ('error_http_status', models.CharField(default=b'200', max_length=4, blank=True)),
                ('error_type', models.CharField(default=b'None', help_text=b'The type of error returned. Can be invalid_request_error, api_error, or card_error', max_length=200, blank=True)),
                ('error_code', models.CharField(default=b'None', help_text=b'For card errors, a short string from amongst those listed on the right describing the kind of card error that occurred.', max_length=200, blank=True)),
                ('error_param', models.CharField(default=b'None', help_text=b'The parameter the error relates to if the error is parameter-specific.', max_length=200, blank=True)),
                ('error_message', models.CharField(default=b'None', help_text=b'A human-readable message giving more details about the error.', max_length=300, blank=True)),
                ('server_message', models.TextField(default=b'', help_text=b'Message detailing internal server errors for debugging purposes', max_length=300, blank=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20, verbose_name='first name', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^[\\w\\s]*$', 32), message='Only letters are allowed.')])),
                ('last_name', models.CharField(max_length=20, verbose_name='last name', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^[\\w\\s]*$', 32), message='Only letters are allowed.')])),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('has_read_conditions', models.BooleanField(default=False, validators=[events.models.registration.validate_true])),
                ('is_email_sent', models.BooleanField(default=False, verbose_name=b'Was the confirmation email sent?')),
                ('staff_comments', models.TextField(default=b'No comments', help_text=b'Log anything to do with this registration here.', max_length=100, blank=True)),
                ('charge', models.ForeignKey(blank=True, to='events.ChargeAttempt', null=True)),
            ],
            options={
                'ordering': ('-updated_at', 'last_name', 'first_name'),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('event', models.OneToOneField(primary_key=True, serialize=False, to='events.Event')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(help_text=b'Required field for event page: http://wearhacks.com/events/<slug>'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path_project, blank=True),
        ),
    ]
