import re
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from django_twilio.client import twilio_client
from django_twilio.decorators import twilio_view
from twilio.twiml import Response

from pledge.models import Election, Pledge
from pledge.forms import PledgeForm

logger = logging.getLogger("debug")

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
        twilio_client.sms.messages.create(to=pledge_.format_phone_number,
                                          from_="+15194898975",
                                          body=election.confirm_txt)
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
    logger.debug("Got a sms request. %s" % unicode(request.POST))
    election = get_object_or_404(Election, date__year=default_year, slug=default_slug)
    r = Response()
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
    #TODO why doesn't one txt in lead to two POSTs to our view?
    #if new == False:
    #    twilio_client.sms.messages.create(to=pledge_.format_phone_number,
    #                                      from_="+15194898975",
    #                                      body="You have already pledged. Thanks!")

    return r