# Generated by Django 4.1.5 on 2023-01-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="section",
            name="unique section for parent",
        ),
        migrations.AddConstraint(
            model_name="section",
            constraint=models.UniqueConstraint(
                fields=("parent_id", "name"), name="unique section for parent"
            ),
        ),
    ]