# Generated by Django 5.0.4 on 2024-04-15 00:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_user_is_active_onetimepassword_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="onetimepassword",
            name="code",
            field=models.CharField(default=410, max_length=6),
        ),
        migrations.AlterField(
            model_name="onetimepassword",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 0, 12, 38, 507584, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
