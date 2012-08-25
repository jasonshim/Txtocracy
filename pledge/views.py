import re

from django.shortcuts import render, redirect, get_object_or_404

from django_twilio.client import twilio_client
from django_twilio.decorators import twilio_view
from twilio.twiml import Response

from pledge.models import Election, Pledge
from pledge.forms import PledgeForm

def home(request, template="home.html"):
    return redirect("pledge", 2012, "ontario")

def election(request, year, slug, template="election.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    return render(request,
                  template,
                  dict(election=election))

def finalize_pledge(request, pledge, election):
    if not Pledge.objects.filter(areacode=pledge.areacode, phone_number=pledge.phone_number).exists():
        pledge.ip = request.META["REMOTE_ADDR"]
        pledge.election = election
        pledge.save()
        twilio_client.sms.messages.create(to=pledge.format_phone_number,
                                          from_="+15194898975",
                                          body=election.confirm_txt)
    # else we already know about the number, so no re-pledging.
    

def pledge(request, year, slug, template="pledge.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    
    if request.method == "POST":
        form = PledgeForm(request.POST)
        if form.is_valid():
            pledge = form.save(commit=False)
            finalize_pledge(request, pledge, election)
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
    phone_number = request.POST.get("From", None)
    if phone_number is None:
        return r
    
    result = phone_re.match(phone_number)
    if result is None:
        return r
    
    areacode, phone_number = result.groups()
    name = request.POST.get("Body", "Joe Public")
    finalize_pledge(request, pledge, election)

    return r