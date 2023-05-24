# Generated by Django 4.1.7 on 2023-05-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_alter_transaction_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[("RECIEVED", "Recieved"), ("PENDING", "Pending")],
                default="PENDING",
                max_length=10,
            ),
        ),
    ]