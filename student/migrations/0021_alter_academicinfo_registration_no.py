# Generated by Django 4.2.2 on 2024-10-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0020_alter_academicinfo_registration_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="academicinfo",
            name="registration_no",
            field=models.IntegerField(default=678729, unique=True),
        ),
    ]
