# Generated by Django 5.1.4 on 2024-12-24 03:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(
                choices=[
                    ("super_admin", "Super Admin"),
                    ("admin", "Admin"),
                    ("staff", "Staff"),
                ],
                default="staff",
                max_length=50,
            ),
        ),
    ]
