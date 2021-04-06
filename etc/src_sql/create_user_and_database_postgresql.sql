
CREATE ROLE covid19data WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	REPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'covid19datapwd';
GRANT pg_execute_server_program, pg_monitor, pg_read_all_settings, pg_read_all_stats, pg_read_server_files, pg_signal_backend TO covid19data WITH ADMIN OPTION;

CREATE DATABASE covid19data
    WITH
    OWNER = covid19data
    TEMPLATE = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'German_Germany.1252'
    LC_CTYPE = 'German_Germany.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE DATABASE covid19data
    WITH
    OWNER = covid19data
    TEMPLATE = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'de_DE.UTF-8'
    LC_CTYPE = 'de_DE.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;




CREATE ROLE tw WITH
	LOGIN
	SUPERUSER
	CREATEDB
	CREATEROLE
	INHERIT
	REPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'Recoil89';
GRANT pg_execute_server_program, pg_monitor, pg_read_all_settings, pg_read_all_stats, pg_read_server_files, pg_signal_backend TO tw WITH ADMIN OPTION;

CREATE DATABASE tw
    WITH
    OWNER = tw
    TEMPLATE = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'de_DE.UTF-8'
    LC_CTYPE = 'de_DE.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;