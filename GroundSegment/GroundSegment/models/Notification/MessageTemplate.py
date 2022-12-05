'''
Created on Sep 27, 2016

@author: ubuntumate
'''
from django.db import models
from GroundSegment.models.Consts import Consts


class MessageTemplate(models.Model):
    """
    Plantilla para la notificacion, al momento de enviar una el mensaje se toma el texto de la plantilla
    se realizan los remplazos por la information asociada (delimitada entre [])  y se genera el texto final.
    
    Ej:
    
        Se ha generado la alarma numero [pk] a hora abordo [dtOnBoard] y es del tipo [alarmaType.code]...etc
    """
    
    name = models.CharField('Nombre de la plantilla', max_length=Consts.smallString, help_text='Nombre de la plantilla', unique=True, default="sin nombre")
    subject = models.CharField('Asunto del mensaje', max_length=Consts.smallString, help_text='Asunto del mensaje', unique=True, default="sin nombre")
    text = models.TextField(null=False, default="Sin mensaje")
    
    
    
    def __str__(self):
        return self.name