# Generated by Django 5.1.4 on 2024-12-24 05:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("igp", "0002_rename_igpitems_igpitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="igp",
            name="description",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="igp",
            name="quantity",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="igp",
            name="sr_no",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="igp",
            name="unit",
            field=models.CharField(default="KG", max_length=50),
        ),
        migrations.AlterField(
            model_name="igp",
            name="messer",
            field=models.CharField(default="staff", max_length=50),
        ),
        migrations.AlterField(
            model_name="igp",
            name="type",
            field=models.CharField(default="Inward", max_length=50),
        ),
        migrations.DeleteModel(
            name="IGPItem",
        ),
    ]
