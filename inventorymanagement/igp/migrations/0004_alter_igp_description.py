# Generated by Django 5.1.4 on 2024-12-24 05:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("igp", "0003_igp_description_igp_quantity_igp_sr_no_igp_unit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="igp",
            name="description",
            field=models.CharField(default="description", max_length=100),
        ),
    ]