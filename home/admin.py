from django.contrib import admin

# Register your models here.
from home.models import Administrator, Domain

admin.site.register(Administrator)
admin.site.register(Domain)