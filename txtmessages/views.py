from django.shortcuts import render, redirect, get_object_or_404

from django_twilio.decorators import twilio_view
from twilio.twiml import Response

from messages.models import Status

@twilio_view
def sms_status_update(request):
    sid = request.POST.get("SmsSid", None)
    status = request.POST.get("SmsStatus", None)
    
    if sid is None or status is None:
        return Response()
    
    try:
        status_obj = Status.objects.get(sid=sid)
    except Status.DoesNotExist:
        status_obj = None
        
    if status_obj is not None:
        status_obj.status = status
        status_obj.save()
    
    return Response()
