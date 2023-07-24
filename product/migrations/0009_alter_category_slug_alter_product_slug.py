# Generated by Django 4.2.1 on 2023-07-03 07:44

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, max_length=255, null=True, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, max_length=255, null=True, populate_from='name', unique=True),
        ),
    ]
