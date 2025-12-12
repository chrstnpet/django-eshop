from .models import Category

def menu_links(request):
    links = Category.objects.filter(parent__isnull=True)
    return dict(links=links)