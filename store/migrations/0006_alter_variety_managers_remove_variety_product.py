# Generated by Django 4.0.6 on 2022-07-30 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_variation_variety'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='variety',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='variety',
            name='product',
        ),
    ]
