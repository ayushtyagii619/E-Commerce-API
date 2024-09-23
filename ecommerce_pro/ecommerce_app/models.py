from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.contrib.postgres.fields import ArrayField

class User(BaseUserManager):
    def create_user(self,email,name,address,mobile,password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            address=address,
            mobile =mobile

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,address,mobile,password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            address=address,
            mobile=mobile
            
        )
        user.is_seller = True
        user.is_admin =True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class NewUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=200,unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    objects = User()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','mobile','address']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price  = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name='products')
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_image/')
    

    def __str__(self):
        return f"Image for {self.product.name}"

class CartItems(models.Model):
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name} - {self.quantity}"
    
    def total_price(self):
        return self.quantity*self.product.price

class OrderItems(models.Model):
    status_choose = [
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    ]
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name='order_items')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    status = models.CharField(max_length=10,choices=status_choose,default='Pending')
    placed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_toatl_price(self):
        cart_items = CartItems.objects.filter(user=self.user)
        total = sum(item.total_price() for item in cart_items)
        self.total_price = total

    def save(self,*args,**kwargs):
        self.get_toatl_price()
        super().save(*args,**kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"
    
class ReviewItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name='review')
    rating = models.IntegerField(choices=[(i , str(i)) for i in range(1 ,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} on {self.product.name}"
    

# Create your models here.
