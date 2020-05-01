from django.contrib import admin

# Register your models here.
from .models import Appointment,Service,Complain

admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Complain)
