from django.db import models

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
    
    def __unicode__(self):
        return self.name
    
class Status(models.Model):
    message = models.ForeignKey(Message)
    receiver = models.ForeignKey("pledge.Pledge")
    status = models.CharField(max_length=64, default="Enqueued")
    
    class Meta:
        verbose_name_plural = "statuses"