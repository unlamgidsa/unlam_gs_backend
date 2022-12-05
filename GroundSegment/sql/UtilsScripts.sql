--Migracion de base de datos entre tablespaces
ALTER DATABASE "DBGS" SET TABLESPACE dbgstablaspace


--Borrado de todos los registros de variables de telemetria 
--de un determinado satelite
delete from public."Telemetry_tlmyvar" as tl 
USING public."Telemetry_tlmyvartype" as tvt, public."GroundSegment_satellite" as sat
Where tl."tlmyVarType_id"=tvt."id" and tvt."satellite_id"=sat."id" and sat."code"='SACD'


--Inners joins ejemplos
select *
from public."Telemetry_tlmyvar" as tl inner join public."Telemetry_tlmyvartype" as tvt on
tl."tlmyVarType_id"=tvt."id" inner join public."GroundSegment_satellite" as sat on
tvt."satellite_id"=sat."id"
where sat."code"='SACD'
Limit 10


select *
from public."Telemetry_tlmyvar" as tl inner join public."Telemetry_tlmyvartype" as tvt on
tl."tlmyVarType_id"=tvt."id" inner join public."GroundSegment_satellite" as sat on
tvt."satellite_id"=sat."id"
where sat."code"='RTEmuSat'
order by tl.id desc
Limit 10


select *
from public."Telemetry_tlmyvartype" as tvt inner join public."GroundSegment_satellite" as sat on
tvt."satellite_id"=sat."id"
where sat."code"='RTEmuSat'
Limit 10



select Count(*)
from public."Telemetry_tlmyvartype"


select count(*)
from public."Telemetry_tlmyvar" as tl inner join public."Telemetry_tlmyvartype" as tvt on
tl."tlmyVarType_id"=tvt."id" inner join public."GroundSegment_satellite" as sat on
tvt."satellite_id"=sat."id"
where sat."code"='RTEmuSat'


-- Index: ix_type_tstamp

-- DROP INDEX IF EXISTS public.ix_type_tstamp;

CREATE INDEX IF NOT EXISTS ix_type_tstamp
    ON public."Telemetry_tlmyvar" USING btree
    ("tlmyVarType_id" ASC NULLS LAST, tstamp ASC NULLS LAST)
    TABLESPACE pg_default;


-- Index: Telemetry_tlmyvar_tlmyVarType_id_ca0d64ee

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvar_tlmyVarType_id_ca0d64ee";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvar_tlmyVarType_id_ca0d64ee"
    ON public."Telemetry_tlmyvar" USING btree
    ("tlmyVarType_id" ASC NULLS LAST)
    TABLESPACE pg_default;


-- Index: Telemetry_tlmyvar_tlmyRawData_id_8e94caab

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvar_tlmyRawData_id_8e94caab";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvar_tlmyRawData_id_8e94caab"
    ON public."Telemetry_tlmyvar" USING btree
    ("tlmyRawData_id" ASC NULLS LAST)
    TABLESPACE pg_default;


--indices quitados



-- Index: Telemetry_tlmyvartype_code_ad40c2a0_like

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_code_ad40c2a0_like";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_code_ad40c2a0_like"
    ON public."Telemetry_tlmyvartype" USING btree
    (code COLLATE pg_catalog."default" varchar_pattern_ops ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_ctype_id_91815d0f

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_ctype_id_91815d0f";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_ctype_id_91815d0f"
    ON public."Telemetry_tlmyvartype" USING btree
    (ctype_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_frameType_id_c627046a

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_frameType_id_c627046a";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_frameType_id_c627046a"
    ON public."Telemetry_tlmyvartype" USING btree
    ("frameType_id" ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_subsystem_id_0307a22a

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_subsystem_id_0307a22a";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_subsystem_id_0307a22a"
    ON public."Telemetry_tlmyvartype" USING btree
    (subsystem_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800"
    ON public."Telemetry_tlmyvartype" USING btree
    ("unitOfMeasurement_id" ASC NULLS LAST)
    TABLESPACE pg_default;



-- 
-- Index: Telemetry_tlmyvartype_code_ad40c2a0_like

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_code_ad40c2a0_like";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_code_ad40c2a0_like"
    ON public."Telemetry_tlmyvartype" USING btree
    (code COLLATE pg_catalog."default" varchar_pattern_ops ASC NULLS LAST)
    TABLESPACE pg_default;


-- Index: Telemetry_tlmyvartype_ctype_id_91815d0f

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_ctype_id_91815d0f";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_ctype_id_91815d0f"
    ON public."Telemetry_tlmyvartype" USING btree
    (ctype_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_frameType_id_c627046a

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_frameType_id_c627046a";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_frameType_id_c627046a"
    ON public."Telemetry_tlmyvartype" USING btree
    ("frameType_id" ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyvartype_subsystem_id_0307a22a

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_subsystem_id_0307a22a";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_subsystem_id_0307a22a"
    ON public."Telemetry_tlmyvartype" USING btree
    (subsystem_id ASC NULLS LAST)
    TABLESPACE pg_default;


-- Index: Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800

-- DROP INDEX IF EXISTS public."Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyvartype_unitOfMeasurement_id_eee4d800"
    ON public."Telemetry_tlmyvartype" USING btree
    ("unitOfMeasurement_id" ASC NULLS LAST)
    TABLESPACE pg_default;


-- Index: Telemetry_tlmyrawdata_satellite_id_state_8233f365_idx

-- DROP INDEX IF EXISTS public."Telemetry_tlmyrawdata_satellite_id_state_8233f365_idx";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyrawdata_satellite_id_state_8233f365_idx"
    ON public."Telemetry_tlmyrawdata" USING btree
    (satellite_id ASC NULLS LAST, state ASC NULLS LAST)
    TABLESPACE pg_default;

-- Index: Telemetry_tlmyrawdata_frameType_id_a7381536

-- DROP INDEX IF EXISTS public."Telemetry_tlmyrawdata_frameType_id_a7381536";

CREATE INDEX IF NOT EXISTS "Telemetry_tlmyrawdata_frameType_id_a7381536"
    ON public."Telemetry_tlmyrawdata" USING btree
    ("frameType_id" ASC NULLS LAST)
    TABLESPACE pg_default;