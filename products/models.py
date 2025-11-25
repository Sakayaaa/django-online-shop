from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify


def upload_to_app(instance, filename):
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    return f'{app_label}/media/{model_name}/{filename}'
# -----------------------------------------------------------------------------------------------------


class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_to_app, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True
# -----------------------------------------------------------------------------------------------------


class Category(BaseModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_children", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)

        if self.parent:
            parent_slug = slugify(self.parent.name)
            new_slug = f"{parent_slug}-{base_slug}"
        else:
            new_slug = base_slug

        if self.slug != new_slug:
            self.slug = new_slug

        super().save(*args, **kwargs)


# -----------------------------------------------------------------------------------------------------


class Brand(BaseModel):
    def __str__(self):
        return super().__str__()

        


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_discounted = models.BooleanField(default=False)
    discounted_price = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
# -----------------------------------------------------------------------------------------------------
