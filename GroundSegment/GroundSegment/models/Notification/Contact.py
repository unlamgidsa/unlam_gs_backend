'''
Created on Sep 27, 2016

@author: ubuntumate
'''

from django.db import models
from GroundSegment.models.Consts import Consts

class Contact(models.Model):
    """
    Contacto/destinatario del las notificaciones. No necesariamente tiene que ser usuario del software del ground segment
    y por tanto se plantea como una entidad separada.
    
    
    @see: Los atributos de esta entidad estan relacionados con los tipos de notificaciones disponibles
    
    @change: Los atributos de esta entidad estan relacionados con los tipos de notificaciones disponibles, al agregar mas tipos 
    de notificaciones puede ser necesario enriquecer esta entidad
    """  
    name = models.CharField('Nombre del contacto', max_length=Consts.smallString, help_text='Nombre del contacto', unique=True)
    email = models.EmailField('EMail del contacto', max_length=Consts.bigString) 
    
    
    
    def __str__(self):
        return self.name