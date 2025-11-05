from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


def upload_to_app(instance, filename):
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    return f'{app_label}/media/{model_name}/{filename}'


class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class MPTTMeta:
        order_insertation_by = ['name']

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    price = models.IntegerField(max_length=9)
    img = models.ImageField(upload_to=upload_to_app)
