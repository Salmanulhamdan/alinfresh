# Generated by Django 4.2.1 on 2023-07-17 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0012_alter_return_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='return',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
