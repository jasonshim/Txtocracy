import uuid
import logging

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django_twilio.client import twilio_client
from twilio import TwilioRestException

logger = logging.getLogger()

class Election(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=140, help_text="this will part of the url.")
    date = models.DateField()
    
    confirm_txt = models.CharField(max_length=160, help_text="This message will be sent to users after they pledge", default="Thanks for pledging to vote.")
    
    information = models.TextField(blank=True, null=True, help_text="Basis of an informational page about the election in markdown.")
    
    def __unicode__(self):
        return self.name
    
class Pledge(models.Model):
    election = models.ForeignKey(Election)
    name = models.CharField(max_length=140, blank=True, null=True)
    areacode = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=7)
    
    exclude = models.BooleanField(default=False, help_text="Check to never show this pledge on the website.")
    voted = models.BooleanField(default=False)
    
    uuid = models.CharField(max_length=128, blank=True)
    ip = models.IPAddressField()
    
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def format_phone_number(self):
        return u"+1" + self.areacode + self.phone_number
    
    def save(self, *args, **kwargs):
        if self.uuid is None or self.uuid == "":
            self.uuid = uuid.uuid1().get_hex()
        super(Pledge, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
#Twilio sucks
class SMS(models.Model):
    sms_message_sid = models.CharField(max_length=60)
    
delete_msg = "TXTOCRACY: Your information has been removed from our system. Thank you for signing up for TXTOCRACY!"
    
@receiver(pre_delete, sender=Pledge)
def handle_pledge_delete(sender, instance, **kwargs):
    try:
        twilio_client.sms.messages.create(to=instance.format_phone_number,
                                          from_="+15194898975",
                                          body=delete_msg)
    except TwilioRestException:
        logger.error('Twilio Rest Exception while sending a deletion message', exc_info=True)
