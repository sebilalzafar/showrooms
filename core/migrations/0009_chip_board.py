# Generated by Django 4.1.7 on 2023-03-31 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_sanitary_ware_product_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chip_Board",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.product",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Waterproof", "Waterproof"),
                            ("Non Waterproof", "Non Waterproof"),
                        ],
                        max_length=50,
                    ),
                ),
                ("size", models.CharField(max_length=50)),
                ("product_number", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Chip Board",
            },
            bases=("core.product",),
        ),
    ]
