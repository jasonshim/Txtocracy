from django.contrib import admin

from txtmessages.models import Message, Status 

class StatusInline(admin.TabularInline):
    model = Status
    extra = 0
    
def send_action(modeladmin, request, queryset):
    for message in queryset:
        message.send()
send_action.short_description = "Send message"

class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "sent", "time_sent", "created", "updated")
    inlines = [StatusInline]
    filter_horizontal = ("custom",)
    actions = [send_action]



admin.site.register(Message, MessageAdmin)