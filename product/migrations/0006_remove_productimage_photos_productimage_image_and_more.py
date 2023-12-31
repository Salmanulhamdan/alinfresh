# Generated by Django 4.2.1 on 2023-06-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_product_image_productimage_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='photos',
        ),
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='', upload_to='multi-image'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='products'),
        ),
    ]
