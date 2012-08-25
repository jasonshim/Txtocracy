from django.shortcuts import render, redirect, get_object_or_404

from django_twilio.client import twilio_client

from pledge.models import Election
from pledge.forms import PledgeForm

def home(request, template="home.html"):
    return redirect("pledge", 2012, "ontario")

def election(request, year, slug, template="election.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    return render(request,
                  template,
                  dict(election=election))

def pledge(request, year, slug, template="pledge.html"):
    election = get_object_or_404(Election, date__year=year, slug=slug)
    
    if request.method == "POST":
        form = PledgeForm(request.POST)
        if form.is_valid():
            pledge = form.save(commit=False)
            pledge.ip = request.META["REMOTE_ADDR"]
            pledge.election = election
            pledge.save()
            twilio_client.sms.messages.create(to=pledge.format_phone_number,
                                              from_="+15194898975",
                                              body=election.confirm_txt)
            return redirect("election", year, slug)
    else:
        form = PledgeForm()
    
    return render(request,
                  template,
                  dict(election=election,
                       form=form))
