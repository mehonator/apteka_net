# Generated by Django 3.2.4 on 2021-07-10 11:24

import autoslug.fields
from django.db import migrations
import logistics.models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitorganization',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=logistics.models.get_slug, unique=True),
        ),
    ]
