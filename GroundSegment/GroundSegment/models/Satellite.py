'''
Created on 16 de ago. de 2016

@author: pablo soligo
'''
import ephem
from ephem import degree
from datetime import *
from requests import *
from sgp4.earth_gravity import wgs72
from django.db import models
from django.utils.timezone import datetime, now, timedelta, utc
from sgp4.io import twoline2rv

from django.db.models.query import QuerySet
from django.db.models import Q
import pytz
from django.dispatch.dispatcher import NONE_ID
from django.db.models.deletion import PROTECT
from sgp4.propagation import false
from CODS.models import ReferenceSystem, Ephemeride
from ephem.tests.test_dates import millisecond
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from Telemetry.models.Calibration import Calibration
from GroundSegment.models.SatelliteState import SatelliteState
from GroundSegment.models.Parameter import Parameter

class Satellite(models.Model):
    
    """
    Clase/Entidad Satelite. 
    """
    
    code           = models.CharField('Codigo del satelite', max_length=24, help_text='Codigo del satelite, ejemplo FS2017', unique=True)
    description    = models.CharField('Decripcion del satelite', max_length=100, help_text='Decripcion del satelite', unique=True)
    noradId        = models.IntegerField('Codigo norad del satelite', help_text='Codigo norad del satelite', unique=True)
    active         = models.BooleanField('Activacion/desactivacion del satelite', default=True)
    state          = models.ForeignKey(SatelliteState, related_name='satellites', on_delete=PROTECT)
    notes          = models.TextField('Observaciones sobre el satelite', max_length=512, null=True) 
    inContact      = models.BooleanField("Si el satelite esta con enlace activo", default=False)
    
    commServerIP            = models.CharField('IP servidor/cortex ', max_length=24, help_text='IP servidor/cortex', default='127.0.0.1')
    commServerPort          = models.CharField('Puerto servidor/cortex', max_length=24, help_text='Puerto servidor/cortex', default='3210')   
    satnogs                 = models.BooleanField("Satelite incorporado a satnogs", default=False)   
    extractDateTimeFun      = models.ForeignKey(Calibration, related_name="extract_datetime_satellites", blank=True, null=True, on_delete=PROTECT)
    extractFrameTypeFun     = models.ForeignKey(Calibration, related_name="extract_frametype_satellites", blank=True, null=True, on_delete=PROTECT)
    extractDateTimeLogic    = None
    extractFrameTypeLogic   = None
    
    
    
    @classmethod
    def new(cls, code, description, noradId, satelliteState=None):
        """
        Constructor de clase
    
        @noradId  m: Identificacion unica asignada por NORAD
        @code m: Codigo unico (unique) del satelite dentro del sistema de segmento terreno MDIAE 2015-2017 
        @description  b: number
        @rtype:   Satellite
        @return:  Nueva instancia del satelite
        """
        
        
        
        result = cls()
        result.code        = code
        result.description = description
        result.noradId     = noradId
        
        result.state       = satelliteState
        
        return result
    
    
    def getEphem(self, epoch=datetime.utcnow()):
        
        #sat.ephems.filter(date__range=["2011-01-01", "2011-01-31"])
        #df = datetime.strptime("30/10/2020", '%d/%M/%Y').replace(tzinfo=pytz.UTC)
        
        epoch = datetime.combine(epoch.date(), time(epoch.hour, epoch.minute, epoch.second, 0)).replace(tzinfo=pytz.UTC)
        #ds = (epoch-timedelta(seconds=0.5)).replace(tzinfo=pytz.UTC)
        #df = (epoch+timedelta(seconds=0.5)).replace(tzinfo=pytz.UTC)
        
        try:
            ephem = self.ephems.get(epoch=epoch)
        except Ephemeride.DoesNotExist:
            #Tengo que propagar
            propagationDetail = self.getCelestialPosition(epoch)
            ephem = Ephemeride()
            ephem.x = propagationDetail.positionX
            ephem.y = propagationDetail.positionY
            ephem.z = propagationDetail.positionZ
            
            ephem.xp = propagationDetail.positionX
            ephem.yp = propagationDetail.positionY
            ephem.zp = propagationDetail.positionZ
            
            ephem.satellite = self;
            ephem.epoch = epoch;
            #Verificar cual es el sistema de referencia de SGP4
            ephem.referenceSystem = ReferenceSystem.objects.get(code="TEME")
            ephem.save()
        except Exception as ex:
            print(ex)
        return ephem;
        
        
        """
        ephems = self.ephems.filter(epoch__range=[ds, df])
        if ephems.count()==0:
            #Tengo que propagar
            propagationDetail = self.getCelestialPosition(epoch)
            ephem = Ephemeride()
            ephem.x = propagationDetail.positionX
            ephem.y = propagationDetail.positionY
            ephem.z = propagationDetail.positionZ
            
            ephem.xp = propagationDetail.positionX
            ephem.yp = propagationDetail.positionY
            ephem.zp = propagationDetail.positionZ
            
            ephem.satellite = self;
            ephem.epoch = epoch;
            #Verificar cual es el sistema de referencia de SGP4
            ephem.referenceSystem = ReferenceSystem.objects.get(code="TEME")
            ephem.save()
            return ephem;
        else:
            #retorno el valor medio
            if ephems.count()>1:
                print("RARO mas de una ephem")
            
            return ephems[ephems.count()//2]
        """
    
    def inEclipse(self, epoch=datetime.utcnow()):
        #Obtener si esta o no en eclipse a partir de su posicion,
        #retorna el tiempo que lleva en eclipse o nulo en caso de no estarlo
        #TODO Implementar este metodo...
        eph = self.getEphem(epoch)
        
        return eph.eclipsed
            
        #ephem.x, ephem.y, ephem.z 
        
   
        
        
        
    
    def eclipseElapsedTime(self, epoch):
        eph = self.getEphem(epoch)
        return eph.secondsInEclipse;
      
    
    def getEclipses(self, startTime, endTime):
        #Codigo repetido, ver como queda mejor
        from GroundSegment.models.Eclipse import Eclipse
        ecs = []
        e=None
        satellite = self      
              
        if endTime < startTime:
           raise Exception("End time should be greater than Start time!")        
        tle=self.getTLE(startTime, endTime)
        
        if tle==None:
            raise Exception("TLE not available")
        
        sat_ephem = ephem.readtle(self.code, tle.getLine1(), tle.getLine2())
        itertime=startTime
        
        while itertime < endTime:
            sat_ephem.compute(itertime)
            if sat_ephem.eclipsed:
                if e == None:
                    e=Eclipse()
                    e.satellite = self
                    e.tle = tle
                    e.startTime=itertime
                else:
                    pass
            else:
                if e==None:
                    pass
                else:
                    e.stopTime=itertime
                    e.obsolete = False
                    e.save()
                    
                    hs = self.eclipses.filter(Q(startTime__range=[e.startTime-timedelta(minutes=5), e.startTime+timedelta(minutes=5)]) and Q(stopTime__range=[e.stopTime-timedelta(minutes=5), e.stopTime+timedelta(minutes=5)])).filter(tleDistance__gt=e.tleDistance)
                    if len(hs)>0:
                        for h in hs:
                            h.obsolete = True
                            h.save()

                    hs = self.eclipses.filter(Q(startTime__range=[e.startTime-timedelta(minutes=5), e.startTime+timedelta(minutes=5)]) and Q(stopTime__range=[e.stopTime-timedelta(minutes=5), e.stopTime+timedelta(minutes=5)])).filter(tleDistance__lte=e.tleDistance).exclude(pk=e.pk)#.exclude(pk=e.pk)
                    if len(hs)>0:
                        e.delete()
                    else:                    
                        pass
                    e=None
   
            itertime=itertime+timedelta(seconds=1)        
        
        return self.eclipses.filter(startTime__gte=startTime, stopTime__lte=endTime, obsolete=False).order_by("startTime")
        
        
    
    def setInContact(self, value):
        self.inContact = value
        return self
   
    
    def getCode(self):
        return self.code
    
    
    """
    Metodo privado doble __
    """
    def __downloadLastTle(self):
        #Solo me traigo el tle si hace un dia que no me lo traigo
        from GroundSegment.models.Tle import Tle
        try:
            loginURL = Parameter.objects.get(key="NoradLoginURL")
        except Parameter.DoesNotExist:
            loginURL = None
            
        if loginURL==None:
            loginURL = Parameter()
            loginURL.key = "NoradLoginURL"
            loginURL.value = "https://www.space-track.org/ajaxauth/login"
            loginURL.module = "Temporal"
            loginURL.save()
            
        try:
            username = Parameter.objects.get(key="NoradUserName")
        except Parameter.DoesNotExist:
            username = None
            
        if username==None:
            username = Parameter()
            username.key = "NoradUserName"
            username.value = "macecilia"
            username.module = "Temporal"
            username.save()
        
        try:
            password = Parameter.objects.get(key="NoradPassword")
        except Parameter.DoesNotExist:
            password = None
            
        if password==None:
            password = Parameter()
            password.key = "NoradPassword"
            password.value = ""
            password.module = "Temporal"
            password.save()
        
            
        data = {'identity': username.value , 'password': password.value}
            
            
        s = session()
        rp = s.post(loginURL.value, data)
        #self.noradId noradid hardcodeado
        fquery = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/" + str(self.noradId) + "/orderby/TLE_LINE1 ASC/format/tle"
        # print(s.cookies)
        rg = s.get(fquery)
            
            
        TLE = rg.text.split("\n")
        sgp4sat = twoline2rv(TLE[0], TLE[1], wgs72)  # es un objeto de clase (satelite)
            
            
        tle = Tle()
        tle.satellite = self
        tle.tleDateTime = sgp4sat.epoch
        tle.downloaded = datetime.now(utc)
        tle.lines = rg.text
        #print("Salvando TLE")
        tle.save()
        
        #param.value = (datetime.now(utc)).strftime("%B %d, %Y")
        #param.save()

    
    def setLastTLE(self, filename):
        """
        Almacena un TLE que no es descargado de NORAD. Tiene como objetivo en etapas de test poder
        operar con TLEs generados artificialmente o poder remplazar un TLE modificado
        #TODO: completar descripcion por ceci
        """
        from GroundSegment.models.Tle import Tle
        #Abro el archivo fisico segun ruta
        file = open(filename, 'r')
        ol = file.read()
        lns = ol.split("\n")
        
        sgp4sat = twoline2rv(lns[0], lns[1], wgs72)  # es un objeto de clase (satelite)
            
            
        tle = Tle()
        tle.satellite = self
        tle.tleDateTime = sgp4sat.epoch
        tle.downloaded = datetime.now(utc)
        tle.lines = ol
        #print("Salvando TLE")
        tle.save()
        
        file.close()
        
        
        
    
    def getLastTLE(self):
        #Implementar que retorne el ultimo TLE, ir a buscar a los TLEs descargado
        """
        Verificar la fecha de ultima descarga del TLE, si puede existir un TLE nuevo intentar descargarlo
        """
        if (self.tles.exists()==False):
            #No hay tle debo descargar el primero
            self.__downloadLastTle()
        else:
            #>>> ds = datetime.date.today()
            #>>> dd = datetime.date(2009, 12, 9)
            #>>> ds - dd
            #datetime.timedelta(2)
            dtn = datetime.now(utc)
            delta = dtn - self.tles.last().tleDateTime
            #print("dif: ", delta.days*24*60)
            if delta.days*24*60>12:
                #print("Tle no actualizado, descargar nuevo tle")
                self.__downloadLastTle()
            else:
                pass
                #TLE actualizado no hago nada! 
                #self.__downloadLastTle()   
                #print("Tle actualizado")
            
            
        return self.tles.last()
    
    
    def __downloadTLEs(self, afrom):
        """
        Retorna el TLE para la fecha pasada como parametro, si
        fueran dos porque estan generados ambos solo retorna el ultimo
        """
        
        result = None
        
        from GroundSegment.models.Tle import Tle
        try:
            loginURL = Parameter.objects.get(key="NoradLoginURL")
        except Parameter.DoesNotExist:
            loginURL = None
            
        if loginURL==None:
            loginURL = Parameter()
            loginURL.key = "NoradLoginURL"
            loginURL.value = "https://www.space-track.org/ajaxauth/login"
            loginURL.module = "Temporal"
            loginURL.save()
            
        try:
            username = Parameter.objects.get(key="NoradUserName")
        except Parameter.DoesNotExist:
            username = None
            
        if username==None:
            username = Parameter()
            username.key = "NoradUserName"
            username.value = "macecilia"
            username.module = "Temporal"
            username.save()
        
        try:
            password = Parameter.objects.get(key="NoradPassword")
        except Parameter.DoesNotExist:
            password = None
            
        if password==None:
            password = Parameter()
            password.key = "NoradPassword"
            password.value = ""
            password.module = "Temporal"
            password.save()
        
        
        data = {'identity': username.value , 'password': password.value}
            
        print("Descargando TLE, deberia ir desapareciendo este mensaje")
            
        s = session()
        rp = s.post(loginURL.value, data)
        #self.noradId noradid hardcodeado
        
        """str(self.noradId)"""
        
        #fquery = "https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/2017-01-01--2017-01-02/NORAD_CAT_ID/37673/orderby/TLE_LINE1%20ASC/format/tle"
        fquery = "https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/"+afrom.strftime("%Y-%m-%d")+"--"+(afrom+timedelta(days=1)).strftime("%Y-%m-%d")+"/NORAD_CAT_ID/"+ str(self.noradId) +"/orderby/TLE_LINE1 ASC/format/tle"
        # print(s.cookies)
        rg = s.get(fquery)
        
        if rg.status_code!=HTTPStatus.OK:
            s.close()
            return None
        s.close()    
        TLE = rg.text.split("\n")
        
        #Tomo de a bloques de a dos
        
        i = 0
        while i<len(TLE)-1:
            sgp4sat = twoline2rv(TLE[i], TLE[i+1], wgs72)  # es un objeto de clase (satelite)
            tle = Tle()
            tle.satellite = self
            tle.tleDateTime = sgp4sat.epoch
            tle.downloaded = datetime.now(utc)
            tle.lines = TLE[i]+"\n"+TLE[i+1]
            
            #print("Salvando TLE")
            
            result = tle
            i+=2    
            
        return result
            
        #param.value = (datetime.now(utc)).strftime("%B %d, %Y")
        #param.save()

    
    
    def getTLE(self, ato):
        """
        Busca el TLE para el dia , en caso de no existir al dia anterior y asi durante todo el rango. 
        Sino encuentra TLE, si pasa una cantidad maxima de dias y no encuentra
        dispara una excepcion. 
        En caso de que la fecha afrom este en el futuro entonces retorna el mas nuevo
        """
        result = None
        
        if ato>datetime.utcnow().replace(tzinfo=pytz.UTC)+timedelta(days=1):
            return self.getLastTLE()
        else:
            
            found = False
            
            started = None
            pivot=ato
            limit=pivot-timedelta(days=5)
            
            while pivot>limit and not found:
                tles = self.tles.filter(validUntil__gte=pivot, validFrom__lte=pivot)
                if len(tles)>0:
                    result = tles.last()
                    #Si busco, no encontro y volvio para atras actualizo hasta donde llega el tle
                    if started!=None:
                        result.validUntil = datetime.combine(started.date(), time(23, 59, 59, 999999)).replace(tzinfo=pytz.UTC)
                        result.save()
                    found = True
                else:
                    result = self.__downloadTLEs(pivot)
                    if result != None:
                        result.validFrom = datetime.combine(pivot.date(), time(0, 0, 0, 0)).replace(tzinfo=pytz.UTC)
                        result.validUntil = datetime.combine(ato.date(), time(23, 59, 59, 999999)).replace(tzinfo=pytz.UTC)
                        
                        
                        result.save()
                        found = True
                        print("TLE para fecha ", pivot, "encontrado");
                    else:
                        print("TLE para fecha ", pivot, "NO ENCONTRADO");
                        started = pivot
            
                
                pivot = pivot - timedelta(days=1)
        
        return result       
    
    def getCelestialPosition(self, dtm=datetime.now(utc)):
        #Implementar el metodo para que retorne la posicion instantane del satelite    
        from GroundSegment.models.Propagation import Propagation
        from GroundSegment.models.PropagationDetail import PropagationDetail
        #if PropagationDetail.objects.all().count()>0:
        #    print(PropagationDetail.objects.last().dt)
        min_dt = (dtm - timedelta(milliseconds=500)).replace(tzinfo=pytz.UTC)
        max_dt = (dtm + timedelta(milliseconds=500)).replace(tzinfo=pytz.UTC)
        #Si ya esta propagado no vuelvo a propagar
        #Asqueroso como se filtra por fecha, no hay forma mejor?? YourModel.objects.filter(datetime_published=datetime(2008, 03, 27))
        prps = PropagationDetail.objects.filter(Q(propagation__satellite=self) and Q(dt__range=(min_dt, max_dt)))
        #.filter(propagation__satellite__code=self.code) 
        #print(prps)
        #Me aseguro de tener TLE
        if prps.count()==0:        
            #self.__downloadLastTle()
            #Si la fecha es en futuro debo buscar el ultimo TLE
            if(dtm>datetime.now(utc)-timedelta(hours=6)):
                tle = self.getLastTLE()
            else:
                tle = self.getTLE(dtm)
            
            
        
            ls = tle.lines.split("\n") 
                
            #print("TLE0:", ls[0])
            #print("TLE1:", ls[1])
            sgp4sat = twoline2rv(ls[0], ls[1], wgs72)

            position, velocity = sgp4sat.propagate(dtm.year, dtm.month, dtm.day, dtm.hour , dtm.minute, dtm.second) #(2000, 6, 29, 12, 50, 19)
            
            propagation = Propagation()
            propagation.tle = tle
            propagation.satellite = self
            propagation.final = False
            
            
            propagationDetail = PropagationDetail()
            propagation.save()
            propagationDetail.propagation = propagation
            
            propagationDetail.positionX = position[0]
            propagationDetail.positionY = position[1]
            propagationDetail.positionZ = position[2]
            
            propagationDetail.velocityX = velocity[0]
            propagationDetail.velocityY = velocity[1]
            propagationDetail.velocityZ = velocity[2]
            propagationDetail.dt = dtm
            
            propagation.save()
            propagationDetail.save()
            
            #print(satellite.error)    # nonzero on error
            #print(satellite.error_message)
            #print(position)
            #(5576.056952..., -3999.371134..., -1521.957159...)
            #print(velocity)
            #(4.772627..., 5.119817..., 4.275553...)
            
            #Primero reviso que la propagacion ya no este realizada
            return propagationDetail
        else:
            
            return prps[0]
        
    def getGeographicPosition(self,afrom,ato):
        satellite = self      
              
        if ato < afrom:
           raise Exception("End time should be greater than Start time!")        
        tle=self.getTLE(afrom, ato)
        
        if tle==None:
            raise Exception("TLE not available")
        
        sat_ephem=ephem.readtle(self.code, tle.getLine1(), tle.getLine2())
        itera_date=afrom
        point=[]
        geoPos=[]

        while itera_date < ato:
            sat_ephem.compute(itera_date)
            point=[sat_ephem.sublat/degree,sat_ephem.sublong/degree]
            geoPos.append(point)
            itera_date=itera_date+timedelta(minutes=1)

        return geoPos
        
    # ALARMAS
    
    def newAlarm(self, alarmType):
        from GroundSegment.models.Alarm import Alarm
        result = Alarm()
        #Por defecto esta en estado pendiente
        result.alarmType = alarmType
        result.satellite = self
        result.save()
        return result
    
    # COMANDOS
    
    def getCommandType(self):
        '''Retorna los tipos de comandos disponibles para este satelite'''
        return self.commandsType.all()
    
    def sendCommand(self, cmd):
        cmd.send()
        
    def sendRTCommand(self, cmdcode, td=5, *args):
        ct = self.getCommandType().get(code=cmdcode)
        cmd = self.newCommand(ct, datetime.utcnow()+timedelta(minutes=td))
        
        if len(args)>0:
            cmd.addParameters(*args)
        self.sendCommand(cmd)
        
        
    def __setExpiredCommands(self):
        #cmds = Command.objects.filter(Q(satellite=self)&Q(expiration__lte=datetime.utcnow().replace(tzinfo=pytz.UTC)    ))
        cmds = self.commands.filter(expiration__lte=datetime.utcnow().replace(tzinfo=pytz.UTC))
        for c in cmds:
            c.setExpirated()
        
        return cmds.count()
    
    def getPendingCommands(self):
        """
        Mato los comandos vencidos
        """
        self.__setExpiredCommands()
        cmds = self.commands.filter(state=0).order_by('executeAt')
        return cmds
        
        
    def expirateAll(self):
        pc = self.getPendingCommands()
        for c in pc:
            c.setExpirated()
        
        return pc.count()
        
    def newCommand(self, commandType, expiration, timetag=datetime.utcnow().replace(tzinfo=pytz.UTC) ):
        from GroundSegment.models.Command.Command import Command

        cmd = Command()
        
        
        if commandType.satellite!=self:
            raise Exception("Este tipo de comando no puede ser aplicado al satelite pasado como parametro")
        
        cmd.satellite    = self
        cmd.commandType  = commandType
        cmd.created      = now()
        cmd.sent         = None
        cmd.retry        = 0
        cmd.expiration   = expiration.replace(tzinfo=pytz.UTC) 
        cmd.executeAt    = timetag.replace(tzinfo=pytz.UTC) 
        #Mejorar la forma en que se trabajan las enumeraciones!
        cmd.state        = 0
        
        return cmd
        
    
    def __str__(self):
        return self.code


   
from django.forms import ModelForm
from django import forms
'''
Herencia del Modelo para crear Formulario
'''
class FormViewSat(ModelForm):
    #description = forms.CharField(error_messages={'required': 'Campo Obligatorio!'})
    class Meta:
        model = Satellite
        fields = "__all__" 
        
        
        
        