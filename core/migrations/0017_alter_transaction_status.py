# Generated by Django 4.1.7 on 2023-05-23 18:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_alter_transaction_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[("RECIEVED", "Recived"), ("PENDING", "Pending")],
                default="PENDING",
                max_length=10,
            ),
        ),
    ]
