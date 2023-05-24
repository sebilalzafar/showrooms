# Generated by Django 4.1.7 on 2023-05-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_transaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="shipping_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
