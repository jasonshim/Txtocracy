import re
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from django_twilio.client import twilio_client
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from twilio import TwilioRestException

from pledge.models import Election, Pledge, SMS
from pledge.forms import PledgeForm

logger = logging.getLogger()

def home(request, template="home.html"):
    return redirect("pledge", 2012, "ontario")

def election(request, year, slug, template="election.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    return render(request,
                  template,
                  dict(election=election))

def finalize_pledge(request, pledge_, election):
    if not Pledge.objects.filter(areacode=pledge_.areacode, phone_number=pledge_.phone_number).exists():
        pledge_.ip = request.META["REMOTE_ADDR"]
        pledge_.election = election
        pledge_.save()
        try:
            twilio_client.sms.messages.create(to=pledge_.format_phone_number,
                                              from_="+15194898975",
                                              body=election.confirm_txt)
        except TwilioRestException:
            logger.error('Twilio Rest Exception while sending confirm message', exc_info=True)
        send_mail("Pledge by %s" % pledge_.name,
                  "Hey\n\nThere is a new pledge in the system by %s.\n\nYou might want to moderate it.\n\nThe system" % pledge_.name,
                  "info@txtocracy.com",
                  ["amjoconn@gmail.com", "jason@jasonshim.net"],
                  fail_silently=True)
        return True
    else:
        return False
    

def pledge(request, year, slug, template="pledge.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    
    if request.method == "POST":
        form = PledgeForm(request.POST)
        if form.is_valid():
            pledge_ = form.save(commit=False)
            new = finalize_pledge(request, pledge_, election)
            if new == False:
                messages.info(request, "According to our recrods you have already pledged. Thanks!")
            return redirect("election", year, slug)
    else:
        form = PledgeForm()
    
    return render(request,
                  template,
                  dict(election=election,
                       form=form))

phone_re = re.compile("\+1(\d{3})(\d{7})")

default_year = 2012
default_slug = "ontario"

@twilio_view
def register_via_sms(request):
    election = get_object_or_404(Election, date__year=default_year, slug=default_slug)
    r = Response()
    
    sms_id = request.POST.get("SmsMessageSid", None)
    if sms_id is None:
        return r
    
    try:
        message = SMS.objects.get(sms_message_sid=sms_id)
        return r
    except SMS.DoesNotExist:
        message = SMS(sms_message_sid=sms_id)
        message.save()
    
    phone_number = request.POST.get("From", None)
    if phone_number is None:
        return r
    
    result = phone_re.match(phone_number)
    if result is None:
        return r
    
    areacode, phone_number = result.groups()
    name = request.POST.get("Body", "Joe Public")
    pledge_ = Pledge(areacode=areacode, phone_number=phone_number, name=name)
    new = finalize_pledge(request, pledge_, election)
    
    if new == False:
        try:
            twilio_client.sms.messages.create(to=pledge_.format_phone_number,
                                              from_="+15194898975",
                                              body="You have already pledged. Thanks!")
        except TwilioRestException:
            logger.error('Twilio Rest Exception while sending already pledged message', exc_info=True)

    return r