# Generated by Django 4.2.1 on 2023-07-08 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0004_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='product_price',
        ),
    ]
