'''
Created on Sep 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Consts import Consts

class NotificationType(models.Model):
    """
    Tipo de notificacion, esta entidad tiene logica asociada e indica el canal de notificacion,
    normalmente email, sms, filereport. Para el FS2017 en su fase academica solo implementa email
    
    @see: En fase academica FS2017 solo se plantea como tipo de notificacion el correo electronico
    @change: En fase academica FS2017 solo se plantea como tipo de notificacion el correo electronico
    """  
    
    code            = models.CharField('Codigo del tipo de notificacion', max_length=Consts.smallString, help_text='Codigo del tipo de notificacion', unique=True)
    """@ivar: This is an instance variable."""
    """
    Codigo mnemonico del tipo de notificacion
    """  
    
    
    description     = models.CharField('Decripcion del tipo de Notificacion', max_length=Consts.mediumString, help_text='Decripcion del tipo de notificacion', unique=True)
    """
    @note: Descripcion del tipo de notificacion
    
    """  
    
    def __str__(self):
        return self.code