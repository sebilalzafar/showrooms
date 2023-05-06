from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid
from django.utils.translation import gettext as _
from datetime import datetime

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
    class Meta:
        verbose_name_plural = 'Showrooms'
        
    def __str__(self):
        return f"{self.showroom_name}({self.showroom_type})"


        
        
 
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
        return f"{self.showroom_type}({self.name})" 

class Company_name(models.Model):
    showroom_type = models.CharField( max_length=50,choices=SHOWROOM_TYPES ,default="")
    name = models.CharField( max_length=50) 
    created_at = models.DateField( auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Company Name'

    def __str__(self):
        return f"{self.showroom_type}({self.name})" 

IMPORTED_OR_LOCAL = (
    ('Imported','Imported'),
    ('Local','Local'),

)




class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 , unique=True)
    showroom = models.ForeignKey(Showrooms, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    image = models.ImageField(upload_to=None , blank=True,null=True)
    company_name = models.ForeignKey(Company_name, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    imported_or_local = models.CharField( max_length=50,choices=IMPORTED_OR_LOCAL ,)
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    discount_price = models.CharField( max_length=50 , blank=True, null=True,default="0% Off")
    description =  models.TextField()
    created_at = models.DateField( auto_now_add=True)
    def __str__(self):
        return f"{self.showroom}({self.name})"     

#================================================Lights
class Lights(Product):
    product_number = models.CharField( max_length=50)
    watt = models.CharField( max_length=50)
    class Meta:
        verbose_name_plural = 'Lights'




#================================================Tiles
class Tiles(Product):
    product_number = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    class Meta:
        verbose_name_plural = 'Tiles'



#================================================Art ANd cultures================================


MADE_BY = (
    ('handmade','handmade'),
    ('machinemade','machinemade'),

)

class Art_And_Culture(Product):
    type = models.CharField( max_length=50,choices=MADE_BY)
    product_number = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    weight = models.CharField( max_length=50 , blank=True,null=True)
    class Meta:
        verbose_name_plural = 'Art And Culture'


#================================================Cars
class Cars(Product):
    type = models.CharField( max_length=50)
    model = models.CharField( max_length=50)
    manufacturing_year = models.CharField( max_length=50)
    registration_year = models.CharField( max_length=50)
    import_year = models.CharField( max_length=50)
    class Meta:
        verbose_name_plural = 'Cars'




#================================================Sanitary Ware
class Sanitary_Ware(Product):
    type = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    product_number = models.CharField( max_length=50)

    class Meta:
        verbose_name_plural = 'Sanitary Ware'


#================================================Chip_Board

TYPE = (
    ('Waterproof','Waterproof'),
    ('Non Waterproof','Non Waterproof'),

)


class Chip_Board(Product):
    type = models.CharField( max_length=50 ,choices= TYPE)
    size = models.CharField( max_length=50)
    product_number = models.CharField( max_length=50)

    class Meta:
        verbose_name_plural = 'Chip Board'
        
        
        
#================================================Marble_Stone
class Marble_Stone(Product):
    product_number = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    class Meta:
        verbose_name_plural = 'Marble Stone'




#================================================SANITARY

SANITARY_TYPE = (
    ('set','set'),
    ('accessories','accessories'),

)

SANITARY_SET_TYPE = (
    ('gold series','gold series'),
    ('silver series','silver series'),

)

class Sanitary(Product):
    type = models.CharField( max_length=50,choices=SANITARY_TYPE)
    accessories_name = models.CharField( max_length=50 , blank=True , null=True)
    set_type = models.CharField( max_length=50,choices=SANITARY_SET_TYPE , blank=True , null=True)
    finshing = models.CharField( max_length=50)
    style = models.CharField( max_length=50)
    product_number = models.CharField( max_length=50)
    size = models.CharField( max_length=50)
    class Meta:
        verbose_name_plural = 'Sanitary'







#====================================cart=============

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)