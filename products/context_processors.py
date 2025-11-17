from .models import Category

def categories_processor(request):
    root_categories = Category.objects.filter(parent__isnull=True)
    return {'root_categories': root_categories}