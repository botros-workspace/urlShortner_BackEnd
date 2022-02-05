from django.contrib import admin
from .models import URL

#To register the url model in the admin panel provided by django
admin.site.register(URL)