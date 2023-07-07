CREATE TABLE public.app_user (
	id bigserial NOT NULL,
	email text NOT NULL,
	updated_at timestamp(0) NOT NULL,
	inserted_at timestamp(0) NOT NULL,
	CONSTRAINT app_user_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX app_user_email_index ON public.app_user USING btree (email);

CREATE TABLE public.subscription (
	id bigserial NOT NULL,
	webhook_url text NOT NULL,
	feed_url text NOT NULL,
	feed_last_entry_id text NULL,
	user_id bigint NOT NULL, 
	updated_at timestamp(0) NOT NULL,
	inserted_at timestamp(0) NOT NULL,
	CONSTRAINT subscription_pkey PRIMARY KEY (id),
	CONSTRAINT subscription_user_id_fkey FOREIGN KEY(user_id) REFERENCES app_user(id)
);