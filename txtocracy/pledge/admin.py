from django.contrib import admin

from pledge.models import Election, Pledge

admin.site.register((Election, Pledge))