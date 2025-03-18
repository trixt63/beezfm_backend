---------------Object---------------------
CREATE TABLE public."object" (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	"type" varchar(50) NOT NULL,
	parent_id int4 NULL,
	location_details jsonb NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT object_pkey PRIMARY KEY (id),
	CONSTRAINT object_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public."object"(id)
);
CREATE INDEX idx_object_parent_id ON public.object USING btree (parent_id);
CREATE INDEX idx_object_type ON public.object USING btree (type);

---------------Datapoint---------------------
CREATE TABLE public.datapoint (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	value varchar NULL,
	unit varchar(50) NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	is_fresh bool DEFAULT true NULL,
	"type" varchar(255) NULL,
	CONSTRAINT datapoint_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_datapoint_name ON public.datapoint USING btree (name);

---------------Object_Datapoint---------------------
CREATE TABLE public.object_datapoint (
	id serial4 NOT NULL,
	"object_FK" int4 NULL,
	"datapoint_FK" int4 NULL,
	last_updated timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT object_datapoint_pkey PRIMARY KEY (id),
	CONSTRAINT unique_object_datapoint UNIQUE ("object_FK", "datapoint_FK"),
	CONSTRAINT object_datapoint_datapoint_id_fkey FOREIGN KEY ("datapoint_FK") REFERENCES public.datapoint(id) ON DELETE CASCADE,
	CONSTRAINT object_datapoint_object_id_fkey FOREIGN KEY ("object_FK") REFERENCES public."object"(id) ON DELETE CASCADE
);
CREATE INDEX idx_od_datapoint_id ON public.object_datapoint USING btree ("datapoint_FK");
CREATE INDEX idx_od_object_id ON public.object_datapoint USING btree ("object_FK");
