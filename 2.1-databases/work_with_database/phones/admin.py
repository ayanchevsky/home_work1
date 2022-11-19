from django.contrib import admin

# Register your models here.
from .models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    ist_display = ['id', 'name', 'image', 'price', 'release_date', 'lte_exists', 'slug']
    list_filter = ['name', 'price']
