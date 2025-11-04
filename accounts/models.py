from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import house_number_validator
from mptt.models import MPTTModel, TreeForeignKey


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=5, validators=[
                              house_number_validator])
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address_summary()} ({self.user.email})"

    def address_summary(self):
        return f"{self.city}, {self.street} {self.number}, {self.postal_code}"


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class MPTTMeta:
        order_insertation_by = ['name']

    def __str__(self):
        return self.name
