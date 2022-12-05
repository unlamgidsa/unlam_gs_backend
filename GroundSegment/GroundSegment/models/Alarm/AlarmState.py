"""@package docstring
Documentation for this module.

More details.
"""

'''
Created on 4 de set. de 2016

@author: Pablo Soligo
'''



from django.db import models




class AlarmState(models.Model):
    """
    
    Clase/Entidad que describe los estados por los que puede pasar una alarma tipicamente:
    
        - Estados
            - Pendiente
            - En Tratamiento
            - Tratada
            
    Entidad sujeta a logica y por tanto solo administrable por personal tecnico de desarrollo    
    """
    
    code            = models.CharField('Codigo del estado de la alarma', max_length=24, help_text='Codigo del estado de la alarma', unique=True)
    description     = models.CharField('Decripcion del estado de la alarma', max_length=100, help_text='Decripcion del estado de la alarma', unique=True)
 

    def __str__(self):
        return self.code