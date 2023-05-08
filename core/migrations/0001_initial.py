# Generated by Django 4.1.7 on 2023-05-08 07:04

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("showroom_owner", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", core.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "showroom_type",
                    models.CharField(
                        choices=[
                            ("Lights", "Lights"),
                            ("Tiles", "Tiles"),
                            ("Art and Culture", "Art and Culture"),
                            ("Cars", "Cars"),
                            ("Sanitary", "Sanitary"),
                            ("Sanitary Ware", "Sanitary Ware"),
                            ("Chip Board", "Chip Board"),
                            ("PVC Piping", "PVC Piping"),
                            ("Marble Stone", "Marble Stone"),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Company_name",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "showroom_type",
                    models.CharField(
                        choices=[
                            ("Lights", "Lights"),
                            ("Tiles", "Tiles"),
                            ("Art and Culture", "Art and Culture"),
                            ("Cars", "Cars"),
                            ("Sanitary", "Sanitary"),
                            ("Sanitary Ware", "Sanitary Ware"),
                            ("Chip Board", "Chip Board"),
                            ("PVC Piping", "PVC Piping"),
                            ("Marble Stone", "Marble Stone"),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Company Name",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("image", models.ImageField(blank=True, null=True, upload_to=None)),
                (
                    "imported_or_local",
                    models.CharField(
                        choices=[("Imported", "Imported"), ("Local", "Local")],
                        max_length=50,
                    ),
                ),
                ("old_price", models.IntegerField()),
                ("new_price", models.IntegerField()),
                (
                    "discount_price",
                    models.CharField(
                        blank=True, default="0% Off", max_length=50, null=True
                    ),
                ),
                ("description", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.categories",
                    ),
                ),
                (
                    "company_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.company_name",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Art_And_Culture",
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
                            ("handmade", "handmade"),
                            ("machinemade", "machinemade"),
                        ],
                        max_length=50,
                    ),
                ),
                ("product_number", models.CharField(max_length=50)),
                ("size", models.CharField(max_length=50)),
                ("weight", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                "verbose_name_plural": "Art And Culture",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Cars",
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
                ("type", models.CharField(max_length=50)),
                ("model", models.CharField(max_length=50)),
                ("manufacturing_year", models.CharField(max_length=50)),
                ("registration_year", models.CharField(max_length=50)),
                ("import_year", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Cars",
            },
            bases=("core.product",),
        ),
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
        migrations.CreateModel(
            name="Lights",
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
                ("product_number", models.CharField(max_length=50)),
                ("watt", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Lights",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Marble_Stone",
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
                ("product_number", models.CharField(max_length=50)),
                ("size", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Marble Stone",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Sanitary",
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
                        choices=[("set", "set"), ("accessories", "accessories")],
                        max_length=50,
                    ),
                ),
                (
                    "accessories_name",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "set_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("gold series", "gold series"),
                            ("silver series", "silver series"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("finshing", models.CharField(max_length=50)),
                ("style", models.CharField(max_length=50)),
                ("product_number", models.CharField(max_length=50)),
                ("size", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Sanitary",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Sanitary_Ware",
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
                ("type", models.CharField(max_length=50)),
                ("size", models.CharField(max_length=50)),
                ("product_number", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Sanitary Ware",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Showrooms",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "showroom_type",
                    models.CharField(
                        choices=[
                            ("Lights", "Lights"),
                            ("Tiles", "Tiles"),
                            ("Art and Culture", "Art and Culture"),
                            ("Cars", "Cars"),
                            ("Sanitary", "Sanitary"),
                            ("Sanitary Ware", "Sanitary Ware"),
                            ("Chip Board", "Chip Board"),
                            ("PVC Piping", "PVC Piping"),
                            ("Marble Stone", "Marble Stone"),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
                ("showroom_name", models.CharField(max_length=50)),
                ("office_phone_number", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=250)),
                ("since", models.CharField(max_length=50)),
                ("link_360", models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                "verbose_name_plural": "Showrooms",
            },
            bases=("core.user",),
            managers=[
                ("objects", core.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Tiles",
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
                ("product_number", models.CharField(max_length=50)),
                ("size", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Tiles",
            },
            bases=("core.product",),
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_quantity", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="showroom",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.showrooms"
            ),
        ),
        migrations.CreateModel(
            name="Callback",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("person_name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=254)),
                ("phone", models.IntegerField()),
                ("reason", models.CharField(max_length=254)),
                ("time", models.TimeField()),
                ("created_at", models.DateField(auto_now_add=True)),
                ("comments", models.CharField(default="", max_length=500)),
                ("called", models.BooleanField(default=False)),
                (
                    "showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.showrooms"
                    ),
                ),
            ],
        ),
    ]
