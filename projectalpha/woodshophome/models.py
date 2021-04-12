from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime

now = datetime.datetime.now()

# Create your models here.
class MyAccountManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email address can't be blank")
        if not username:
            raise ValueError("user name filed can't be blank")
        user=self.model(
            email=self.normalize_email(email),
            username=self.username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    


class Account(AbstractUser):
    email=models.EmailField(verbose_name='email')
    mobile_number=models.BigIntegerField(default=91)
    username=models.CharField(max_length=20, unique=True)
    date_joined=models.DateField(null=True)
    last_login=models.DateField(null=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS=['mobile_number']


class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, )
    #user_id= models.CharField(max_length=20,default=None)

class Order(models.Model):
    order_id=models.CharField(max_length=20)
    order_item=models.CharField(max_length=200)
    username=models.ForeignKey(Account,on_delete=models.CASCADE)
    order_status=models.CharField(max_length=200, default='New')
    order_desc=models.CharField(max_length=200)
    order_unit=models.CharField(max_length=200, default=0)
    order_date=models.DateField(default=None, null=True)

class Stock(models.Model):
    product_name=models.CharField(max_length=200)
    product_details=models.CharField(max_length=500)
    in_stock=models.BooleanField()
    available_quantity=models.BigIntegerField()
    unit_of_measure=models.CharField(max_length=200)

class Procucts(models.Model):
    product_id=models.CharField(max_length=20, unique=True)
    product_name=models.CharField(max_length=50)
    product_brand=models.CharField(max_length=50)
    product_model=models.CharField(max_length=50)
    product_description=models.CharField(max_length=100)
    product_rating=models.FloatField()
    prduct_img_path=models.CharField(max_length=1000,default='not_available')

class ProdductPrice(models.Model):
    product_id=models.ForeignKey(Procucts,on_delete=models.DO_NOTHING, default=0)
    price=models.FloatField()
    pricicin_unit=models.CharField(max_length=20)