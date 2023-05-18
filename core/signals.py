from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Assuming you have a User model for the shop owners
from .models import Showrooms, showroom_settings  # Replace "Shop" and "ShopSettings" with your actual models


@receiver(post_save, sender=Showrooms)
def create_shop_settings(sender, instance, created, **kwargs):
    if created:
        showroom_settings.objects.create(showroom=instance)
