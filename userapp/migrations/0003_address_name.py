# Generated by Django 4.2.1 on 2023-06-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
