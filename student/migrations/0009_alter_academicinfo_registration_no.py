# Generated by Django 4.2.2 on 2024-10-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("student", "0008_alter_academicinfo_registration_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="academicinfo",
            name="registration_no",
            field=models.IntegerField(default=785790, unique=True),
        ),
    ]
