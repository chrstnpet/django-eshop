from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display    = ('category_name', 'parent')
    list_filter     = ('parent')
    search_fields   = ('category_name')
    ordering        = ('parent', 'category_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs["queryset"]  = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)