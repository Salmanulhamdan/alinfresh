
import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from decimal import Decimal
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email,password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=15,null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()






# user address: user have multiple addresses

User=get_user_model()
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length=100,null=True)
    house = models.CharField(max_length=50)
    pincode = models.IntegerField(null=True)
    place= models.CharField(max_length=50)
    address_line = models.CharField(max_length=50, blank=True)
    ultranate_phone=models.CharField(max_length=15,null=True)
    
    


    def __str__(self):
        return str(self.name)
    





#model for wallet


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    def __str__(self):
        return f"Wallet for {self.user.username}"
    

    def apply_wallet_amount(self, total_price):
    #     print(total_price)
    #     # Calculate the maximum amount that can be reduced from the total price
    #     wallet_balance = Decimal('40.0')

    # # Calculate the maximum amount that can be reduced from the total price
    #     max_reduction = min(Decimal(total_price), wallet_balance * Decimal('0.5'))
    #     print("mm",max_reduction)
    #     print(wallet_balance)
        if self.balance >= total_price/2:
            max_reduction=total_price/2
        else:
            max_reduction=Decimal(self.balance)
        print("mm",max_reduction)


        if max_reduction > 0:
            # Update the wallet balance and reduce the amount from the wallet
            self.balance -= Decimal(max_reduction)
            self.save()

        return max_reduction