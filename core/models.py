from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid
from django.utils.translation import gettext as _
from datetime import datetime
import random
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 , unique=True)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    showroom_owner = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

SHOWROOM_TYPES = (
    ('Lights','Lights'),
    ('Tiles','Tiles'),
    ('Art and Culture','Art and Culture'),
    ('Cars','Cars'),
    ('Sanitary','Sanitary'),
    ('Sanitary Ware','Sanitary Ware'),
    ('Chip Board','Chip Board'),
    ('PVC Piping','PVC Piping'),
    ('Marble Stone','Marble Stone'),
)


class Showrooms(User):
    showroom_type = models.CharField( max_length=50,choices=SHOWROOM_TYPES ,default="")
    showroom_name = models.CharField( max_length=50)
    office_phone_number = models.CharField( max_length=50)
    address = models.CharField( max_length=250)
    since = models.CharField( max_length=50)
    link_360 = models.CharField( max_length=250 , blank=True,null=True)
    google_analytics_link = models.CharField( max_length=3000 , blank=True,null=True)
    class Meta:
        verbose_name_plural = 'Showrooms'
        
    def __str__(self):
        return f"{self.showroom_name}({self.showroom_type})"


class Node_visitors(models.Model):
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE, related_name='node_visitors_showrooms')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='node_visitors_users')  
    node = models.CharField( max_length=50,blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)




class showroom_settings(models.Model):
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE)  
    shop_logo = models.ImageField( upload_to="shop_logo", default="shop_logo/default_shop_logo.png", blank=True , null = True ) 
    address = models.CharField(max_length=250, blank=True , null = True , default="Set your address in shop settings")
    email = models.CharField( max_length=50, blank=True , null = True , default="Set your email in shop settings")
    phone = models.CharField( max_length=50 , blank=True , null = True , default="Set your phone in shop settings") 
    android_app_link = models.CharField( max_length=250 , default = "#")    
    ios_app_link = models.CharField( max_length=250 , default = "#") 
    facebook = models.CharField( max_length=50 , default = "#")   
    instagram = models.CharField( max_length=50 , default = "#")   
    twitter = models.CharField( max_length=50 , default = "#")   

 
class Callback(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 , unique=True)
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE)
    person_name = models.CharField( max_length=50)
    email = models.CharField(max_length=254)
    phone = models.IntegerField()
    reason = models.CharField(max_length=254)
    time  = models.TimeField( auto_now_add=False)
    created_at = models.DateField( auto_now_add=True)
    comments = models.CharField( max_length=500,default="")
    called = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.person_name}({self.showroom})"            


#Products Model

class Categories(models.Model):
    showroom_type = models.CharField( max_length=50,choices=SHOWROOM_TYPES ,default="")
    name = models.CharField( max_length=50) 
    created_at = models.DateField( auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}" 

class Company_name(models.Model):
    showroom_type = models.CharField( max_length=50,choices=SHOWROOM_TYPES ,default="")
    name = models.CharField( max_length=50) 
    created_at = models.DateField( auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Company Name'

    def __str__(self):
        return f"{self.name}" 

IMPORTED_OR_LOCAL = (
    ('Imported','Imported'),
    ('Local','Local'),

)




class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 , unique=True)
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    image = models.ImageField(upload_to="products" )
    company_name = models.ForeignKey(Company_name, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_number = models.CharField( max_length=50)
    imported_or_local = models.CharField( max_length=50,choices=IMPORTED_OR_LOCAL ,)
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    discount_price = models.CharField( max_length=50 , blank=True, null=True,default="0% Off")
    description =  models.TextField()
    created_at = models.DateField( auto_now_add=True)
    def __str__(self):
        return f"{self.showroom}({self.title})"     




#====================CART and order item fuctionality functionaity=================================


class Order(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE , related_name="showrooms")
    products_list = models.CharField(max_length=250 , blank= True , null = True)
    total_amount = models.CharField(max_length=250 , blank= True , null = True)
    first_name = models.CharField( max_length=50 , blank=True , null=True)
    last_name = models.CharField( max_length=50 ,blank=True , null=True)
    street_address = models.CharField( max_length=200,blank=True , null=True)
    city = models.CharField( max_length=50,blank=True , null=True)
    phone = models.IntegerField(blank=True , null=True)
    email = models.EmailField(max_length=254,blank=True , null=True)
    order_description = models.TextField(blank=True , null=True)
    ordered = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'

    
    
    

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('RECIEVED', 'Recieved'),
        ('PENDING', 'Pending'),
    )
    transaction_id = models.CharField(max_length=10, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount =models.PositiveIntegerField(blank=True,null=True)
    shipping_amount = models.PositiveIntegerField(blank=True,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    # Add more fields as per your requirements

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)

    def generate_transaction_id(self):
        return str(random.randint(1000000000, 9999999999))