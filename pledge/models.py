import uuid
from django.db import models

class Election(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=140, help_text="this will part of the url.")
    date = models.DateField()
    
    information = models.TextField(blank=True, null=True, help_text="Basis of an informational page about the election in markdown.")
    
    def __unicode__(self):
        return self.name
    
class Pledge(models.Model):
    election = models.ForeignKey(Election)
    name = models.CharField(max_length=140, blank=True, null=True)
    areacode = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=7)
    
    voted = models.BooleanField(default=False)
    
    uuid = models.CharField(max_length=128, blank=True)
    ip = models.IPAddressField()
    
    def save(self, *args, **kwargs):
        if self.uuid is None or self.uuid == "":
            self.uuid = uuid.uuid1().get_hex()
        super(Pledge, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name