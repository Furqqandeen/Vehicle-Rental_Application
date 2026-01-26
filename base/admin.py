from django.contrib import admin
from .models import Vehicle,Rental,Profile,Category

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Rental)
admin.site.register(Profile)
admin.site.register(Category)
