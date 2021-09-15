from django.contrib import admin

from apiback.models import Street, City, Shop

admin.site.register(City)
admin.site.register(Street)
admin.site.register(Shop)
