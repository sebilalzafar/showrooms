# Generated by Django 4.1.7 on 2023-05-12 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
