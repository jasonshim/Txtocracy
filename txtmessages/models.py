import datetime

from django.db import models
from django.core.urlresolvers import reverse

from django_twilio.client import twilio_client

from pledge.models import Pledge

class Message(models.Model):
    """
    Represent a SMS message which can be
    sent to a lot of people via Twilio
    """
    
    TO_CHOICES = (
        ("Everyone", "Everyone"),
        ("Non Voters", "Everyone who hasn't voted"),
        ("Custom", "Custom")
    )
    
    name = models.CharField(max_length=128)
    to_type = models.CharField(max_length=64, choices=TO_CHOICES, default="Everyone")
    custom = models.ManyToManyField("pledge.Pledge", blank=True, null=True, help_text="Only used if to type is custom")
    
    message = models.TextField()
    
    sent = models.BooleanField(default=False)
    
    time_sent = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def send(self):
        if not self.sent:
            self.sent = True
            self.time_sent = datetime.datetime.now()
            self.save()
            import pdb; pdb.set_trace()
            to_list = self.get_to_list()
            
            for pledge_ in to_list:
                # We are going to hit twilio rapidly, but it will queue message
                # and send one a second
                resp = twilio_client.sms.messages.create(to=pledge_.format_phone_number,
                                                         from_="+15194898975",
                                                         body=self.message,
                                                         status_callback=reverse('sms_status_update'))
                new_status = Status(message=self,
                                   receiver=pledge_,
                                   sid=resp.sid)
                new_status.save()
            
    def get_to_list(self):
        if self.to_type == "Everyone":
            return Pledge.objects.all()
        elif self.to_type == "Non Voters":
            return Pledge.objects.filter(voted=False)
        else:
            return self.custom.all()
    
    def __unicode__(self):
        return self.name
    
class Status(models.Model):
    message = models.ForeignKey(Message)
    receiver = models.ForeignKey("pledge.Pledge")
    sid = models.CharField(max_length=64)
    status = models.CharField(max_length=64, default="Queued")
    
    class Meta:
        verbose_name_plural = "statuses"