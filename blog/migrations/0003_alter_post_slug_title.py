# Generated by Django 5.0 on 2023-12-24 12:56

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug_title',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=200, populate_from='title', unique=True, verbose_name='Post slug'),
        ),
    ]
