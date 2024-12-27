# Generated by Django 5.1.4 on 2024-12-27 03:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("type", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="type",
            name="description",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="type",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]