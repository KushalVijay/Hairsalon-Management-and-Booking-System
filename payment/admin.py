from django.contrib import admin

# Register your models here.
from .models import Invoice,Salarie
admin.site.register(Invoice)
admin.site.register(Salarie)
