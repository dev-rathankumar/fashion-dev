from .models import Category

def category_names(request):
    category = Category.objects.all()
    quickshopCat = Category.objects.filter(parent=None).order_by('id')[:10]
    return dict(category=category, quickshopCat=quickshopCat)
