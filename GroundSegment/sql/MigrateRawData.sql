insert into "Telemetry_tlmyrawdata"
(created, pktdatetime, 
 data, source, "dataLen", 
 state, satellite_id, 
 "capturedAt", strdata, 
 "abortedError", "processedTime",
 "realTime")
select  uhf.created, 
        uhf.created, 
        uhf.data, 
        uhf.source, 
        uhf."dataLen" as "dl", 
        1 as "state", 
        1 as "satellite_id",
        uhf.created,
        '' as strdata,
        '' as abortedError,
        0 as processedTime,
        true as realTime
from "FS2017_uhfrawdata" as uhf
where upper(source)!=upper('simulation')