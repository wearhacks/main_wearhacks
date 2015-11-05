# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20151013_0327'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamMembers',
            new_name='TeamMember',
        ),
    ]
