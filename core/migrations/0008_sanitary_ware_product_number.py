# Generated by Django 4.1.7 on 2023-03-31 15:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_sanitary_ware_rename_car_model_cars_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="sanitary_ware",
            name="product_number",
            field=models.CharField(default="22222", max_length=50),
            preserve_default=False,
        ),
    ]
