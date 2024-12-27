# Generated by Django 5.1.4 on 2024-12-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("igp", "0006_alter_igp_vehicle_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="igp",
        ),
        migrations.AddField(
            model_name="item",
            name="igp",
            field=models.ManyToManyField(related_name="items", to="igp.igp"),
        ),
    ]