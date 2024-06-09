"""
"""

QUERIES = {
	"table_name": {
		"DROP": """
			DROP TABLE IF EXISTS public.table_name;
		""",
		"CREATE": """
			CREATE TABLE IF NOT EXISTS public.table_name (
				nstudentid int8 NOT NULL,
				strfullname varchar NOT NULL,
				nmobileno int8 NOT NULL,
				stremailid varchar NOT NULL,
				nstatus int4 NULL DEFAULT 1,
				dtcreated TIMESTAMP NOT NULL,
				strcreatedby varchar NOT NULL,
				dtupdated TIMESTAMP NULL,
				strupdatedby varchar NULL,
				CONSTRAINT table_name_pk PRIMARY KEY (nstudentid)
			);
			CREATE INDEX table_name_dtcreated_idx ON table_name USING btree(dtcreated);
			DROP SEQUENCE IF EXISTS public.table_name_seq CASCADE;
			CREATE SEQUENCE public.table_name_seq
				INCREMENT BY 1
				MINVALUE 0
				MAXVALUE 9223372036854775807
				START 1
				CACHE 1
				NO CYCLE;
		""",
		"INSERT": """
		""",
		"UPDATE": """
		""",
		"DELETE": """
		"""
	}
}