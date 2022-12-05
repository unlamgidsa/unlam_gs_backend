from django.db import models

class Parameter(models.Model):
    module         = models.CharField('Modulo', max_length=64, help_text='Modulo donde normalmente se usuario el parametro' )
    key            = models.CharField('Clave', max_length=24, help_text='Clave' )
    value          = models.CharField('Valor', max_length=128, help_text='Valor del parametro' )
    description    = models.TextField('Descripcion', help_text='Descripcion del parametro, donde se usa, para que?' , default='Describir parametro aqui')
    
        
        
    @classmethod
    def create(cls, module, key, value, description):
        param = cls()
        # do something with the book
         
        param.module         =  module
        param.key            =  key
        param.value          =  value
        param.description    =  description
        return param
    
        
    
  
    def __str__(self):
        return self.module+","+self.key+","+self.value
    
    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value

