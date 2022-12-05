from django import forms
from GroundSegment.models.Satellite import Satellite
from django.utils.timezone import datetime, now, timedelta, utc


class SimulatorForm(forms.Form):
    
    def simulateAlarm(self):
        pass
    
    
    
class PropagateTestForm(forms.Form):
    
    #name = forms.CharField()
    #message = forms.CharField(widget=forms.Textarea)

    def propagate(self):
        
        #sat = Satellite.objects.get(noradId="")
        sat = Satellite.objects.get(code="FS2017")
        satgeo = Satellite.objects.get(code="FS2021")
        

        
        dt = datetime.now(utc)
        
        for i in range(3600):
            dt = dt+timedelta(seconds=1)
            satgeo.getCelestialPosition(dt)
        
        dt = datetime.now(utc)
        for i in range(3600):
            dt = dt+timedelta(seconds=1)
            sat.getCelestialPosition(dt)
        
        
        #print("Form execution")
        #print("Celestial position 1: ", sat.getCelestialPosition(dt))
        
        
        #Vuelvo a pedir, no deberia propagar!!!
        #print("Celestial position 2: ", sat.getCelestialPosition(dt))