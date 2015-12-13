# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='short_name',
        ),
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path_event, validators=[events.models.helpers.validate_large_image]),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(help_text=b'ie: Short name, required field for event page: http://wearhacks.com/events/<slug>'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='partner_type',
            field=models.CharField(max_length=1, choices=[(b'0', b'Global Partners'), (b'1', b'Hardware Partners'), (b'2', b'Media Partners'), (b'3', b'Ecosystem Partners'), (b'4', b'Legal Partners'), (b'5', b'Previous City Partners')]),
        ),
        migrations.AlterField(
            model_name='partner',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path, validators=[events.models.helpers.validate_small_image]),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path_project, blank=True),
        ),
        migrations.AlterField(
            model_name='slider',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path, validators=[events.models.helpers.validate_large_image]),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=events.models.helpers.get_upload_path, validators=[events.models.helpers.validate_small_image]),
        ),
    ]
