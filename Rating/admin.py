from django.contrib import admin
from .models import Rating
# Register your models here.


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment',  'created_on')


admin.site.register(Rating, RatingAdmin)
