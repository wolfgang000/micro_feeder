CREATE TABLE public.app_user (
	id bigserial NOT NULL,
	email text NOT NULL,
	updated_at timestamp(0) NOT NULL,
	inserted_at timestamp(0) NOT NULL,
	CONSTRAINT app_user_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX app_user_email_index ON public.app_user USING btree (email);