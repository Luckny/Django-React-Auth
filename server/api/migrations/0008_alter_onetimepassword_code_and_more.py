# Generated by Django 5.0.4 on 2024-04-21 16:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_onetimepassword_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="code",
            field=models.CharField(default="4EB603", max_length=6),
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 21, 17, 2, 16, 257803, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]