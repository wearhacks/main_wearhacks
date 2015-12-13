# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import events.models.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151208_0224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(default=0)),
                ('photo', models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path, blank=True)),
                ('main_text', models.TextField()),
                ('first_link_text', models.CharField(max_length=50, blank=True)),
                ('first_link', models.URLField(max_length=100, blank=True)),
                ('second_link_text', models.CharField(max_length=50, blank=True)),
                ('second_link', models.URLField(max_length=100, blank=True)),
                ('overlay_percentage', models.DecimalField(default=0, help_text=b'Specify background opacity 0~>1.  0 -> Clear image, 1-> completely dark', max_digits=2, decimal_places=2)),
                ('align_left', models.BooleanField(default=False)),
                ('add_call_to_action', models.BooleanField(default=False)),
                ('slider_location', models.CharField(default=0, max_length=1, choices=[(b'0', b'MAIN PAGE'), (b'1', b'MISSION PAGE'), (b'2', b'AMBASSADOR PAGE')])),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(help_text=b'Required field for event page: http://wearhacks.com/events/<slug>'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='partner_type',
            field=models.CharField(max_length=1, choices=[(b'0', b'Global Partners'), (b'1', b'Hardware Partners'), (b'2', b'Media Partners'), (b'3', b'Ecosystem Partners'), (b'4', b'Legal Partners'), (b'5', b'Previous City Partners')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=events.models.helpers.get_upload_path_project, blank=True),
        ),
    ]
