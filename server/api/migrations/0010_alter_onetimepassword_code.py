# Generated by Django 5.0.4 on 2024-04-21 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_alter_onetimepassword_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimepassword",
            name="code",
            field=models.CharField(default="8DD91D", max_length=6),
        ),
    ]
