# Generated by Django 4.2.1 on 2023-07-05 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_productvariant_quantity_in_stock_and_more'),
        ('cart', '0009_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productvariant'),
        ),
    ]
