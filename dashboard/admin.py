from django.contrib import admin

from .models import Document, Rents

# Register your models here.
admin.site.register([Document, Rents])