# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leaf_loc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LazySpot',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('geom', djgeojson.fields.PointField()),
                ('description', models.TextField()),
            ],
        ),
    ]
