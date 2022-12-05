'''
Created on 4 de set. de 2016

@author: Pablo Soligo
'''

from django.db import models



class Criticity(models.Model):
    """
    Criticidad del evento o la alarma. Define el nivel de gravedad y atributos asociados, tipicamente
        -Gravedad
        -Color
        -Sonido
        -etc
    
    """
    
    
    code           = models.CharField('Codigo de criticidad', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description    = models.CharField('Decripcion de la criticidad', max_length=100, help_text='Decripcion del satelite', unique=True)
    color          = models.CharField(max_length=7, default="#FF0000")
    sound          = models.FileField("/media")
    # docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
    
    def __str__(self):
        return self.code+", "+self.description
    
    
    class Meta:
        verbose_name        = "Criticidad"
        verbose_name_plural = "Criticidades"
    
    
    