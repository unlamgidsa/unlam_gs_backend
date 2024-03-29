from django.db import models
# Create your models here.
class WSClient(models.Model):
    ipv4            = models.CharField('Ipv4', max_length=24, help_text='ipv4', default="")
    port            = models.IntegerField('port', default=0)
    lastConnection  = models.DateTimeField(auto_now_add=True)
    




class SubscribedTlmyVar(models.Model):
    fullname = models.CharField('fullname', max_length=64, help_text='var name satellite.tlmyvar', default="")
    wsClient = models.ForeignKey('WSClient', related_name="subscribedTlmyVar", on_delete=models.CASCADE)