# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20151121_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-pinned', '-id')},
        ),
        migrations.AddField(
            model_name='project',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
