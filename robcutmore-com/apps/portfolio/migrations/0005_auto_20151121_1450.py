# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20151121_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
