# Generated by Django 5.1.4 on 2024-12-24 05:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("igp", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="IGPItems",
            new_name="IGPItem",
        ),
    ]