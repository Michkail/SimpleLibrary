# Generated by Django 4.2.16 on 2024-09-21 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowedbook",
            name="return_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 10, 21, 12, 53, 40, 799712, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
