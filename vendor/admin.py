from django.contrib import admin
from . import models 


# Register your models here.

admin.site.register(models.vendor)
admin.site.register(models.company)
admin.site.register(models.address)
admin.site.register(models.otp)
