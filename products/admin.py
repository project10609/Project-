from django.contrib import admin
from .models import *


class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category', 'slug')
    ordering = ('-category',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(Subcategories, SubCategoriesAdmin)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Source)
