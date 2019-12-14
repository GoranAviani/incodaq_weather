from django.contrib import admin

# Register your models here.
from .models import default_cities

class default_cities_admin (admin.ModelAdmin):
    model = default_cities
    list_display = ("city", "temperature", "weatherIconDesc")

admin.site.register(default_cities, default_cities_admin)