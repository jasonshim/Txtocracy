from django.contrib import admin

from messages.models import Message, Status 

class StatusInline(admin.TabularInline):
    model = Status
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "sent", "time_sent", "created", "updated")
    inlines = [StatusInline]

admin.site.register(Message, MessageAdmin)