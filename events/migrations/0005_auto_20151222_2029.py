# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_pastevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventExtend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(help_text=b'Extension value', max_length=b'250')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventExtendType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'Keyword to name this extension.', max_length=b'50')),
                ('description', models.CharField(help_text=b'Short description of what this extensions is about.', max_length=b'250')),
                ('values', models.CharField(help_text=b'Allowed values (for list, delimetered by comma.', max_length=b'250', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtendType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(help_text=b'Number, Text, List, ...', max_length=b'50')),
            ],
        ),
        migrations.AddField(
            model_name='eventextendtype',
            name='type',
            field=models.ForeignKey(to='events.ExtendType'),
        ),
        migrations.AddField(
            model_name='eventextend',
            name='extendKey',
            field=models.ForeignKey(help_text=b'Extension key', to='events.ExtendType'),
        ),
    ]
