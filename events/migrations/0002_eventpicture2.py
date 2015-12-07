# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_username', models.CharField(max_length=50)),
                ('source_albumname', models.CharField(max_length=50)),
                ('source_type', models.CharField(max_length=1, choices=[(b'0', b'Other'), (b'1', b'flickr')])),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
    ]
