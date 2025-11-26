from django.contrib import admin
from .models import Category, Product, Brand
from mptt.admin import DraggableMPTTAdmin

admin.site.register([Product, Brand])
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    list_display_links=('indented_title',),
)
