# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_persona_estatura'),
    ]

    operations = [
        migrations.DeleteModel(
            name='persona',
        ),
    ]
