# Python script to import data from the [Coronavirus (COVID-19) repository](https://github.com/CSSEGISandData/COVID-19)

*Note: There currently is an issue with importing CSV files where if theres a comma contained within double quotes, it seems to parse it.
This line breaks it for now: `'"Chicago, IL",US,2/1/2020 19:43,2,0,0'`

***
## Installation
- create a DB and specify the details in the `data_scraper.py` script
- create the 2 tables and unique index in the database:

`CREATE TABLE public.daily_files_processed
(
    id bigint NOT NULL DEFAULT nextval('daily_files_processed_id_seq'::regclass),
    file_name text COLLATE pg_catalog."default" NOT NULL,
    created timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT daily_files_processed_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
`

`CREATE UNIQUE INDEX daily_files_processed_file_name_idx
    ON public.daily_files_processed USING btree
    (file_name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;`


`CREATE TABLE public.world_data
(
    id bigint NOT NULL DEFAULT nextval('world_data_id_seq'::regclass),
    province_state text COLLATE pg_catalog."default",
    country_region text COLLATE pg_catalog."default" NOT NULL,
    last_update_in_utc timestamp without time zone NOT NULL,
    confirmed integer,
    deaths integer,
    recovered integer,
    latitude numeric,
    longitude numeric,
    created timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT world_data_id_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
`
***
## Running it
- clone the COVID-19 data repo and change the path in the script
- just excute in the command line:  `python3 data_scraper.py`