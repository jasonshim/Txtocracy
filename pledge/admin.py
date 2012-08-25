from django.contrib import admin

from pledge.models import Election, Pledge

class PledgeAdmin(admin.ModelAdmin):
    list_display = ("name", "election", "areacode", "phone_number", "created", "ip", "voted")

admin.site.register(Election)
admin.site.register(Pledge, PledgeAdmin)