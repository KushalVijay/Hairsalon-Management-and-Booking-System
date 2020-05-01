from django.contrib import admin

# Register your models here.
from .models import Store,Client,Employee
from django.contrib.auth.models import User,Group
admin.site.register(Store)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.unregister(User)
admin.site.unregister(Group)
