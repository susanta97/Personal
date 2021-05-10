from django.contrib import admin

from .models import MyProfile, City, Country, MyAddress

admin.site.register(MyProfile)

admin.site.register(City)
admin.site.register(Country)

admin.site.register(MyAddress)
