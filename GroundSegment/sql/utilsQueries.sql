select *
from groundSegment_tle
where groundSegment_tle.satellite_id=3

delete from groundSegment_propagationdetail;
delete from groundSegment_propagation;

select groundSegment_propagationdetail.dt, groundSegment_propagationdetail.earthDistance
from groundSegment_propagationdetail inner join groundSegment_propagation on groundSegment_propagation.id=groundSegment_propagationdetail.propagation_id
where groundSegment_propagation.satellite_id=3 and groundSegment_propagationdetail.earthDistance<>0


select *
from "GroundSegment_uhfrawdata" as uhf
where length(uhf.data)>32


insert into public."GroundSegment_uhfrawdata" (created, data, source)
SELECT t1.created, t1.ndata, t1.source
    FROM dblink('dbname=DBGroundSegment_tmp', 'select created, data as ndata, source from "GroundSegment_uhfrawdata"')
      AS t1(created timestamp,ndata bytea,source text)

      
      
//Copiado de telemetria a arhivo
COPY (select uhf.data from "GroundSegment_uhfrawdata" as uhf where uhf.id=1002) TO 'c:\temp\tlmy1.data' (FORMAT binary)





