CREATE TABLE public.subscription (
	id bigserial NOT NULL,
	webhook_url text NOT NULL,
	feed_url text NOT NULL,
	feed_last_entry_id text NULL,
	updated_at timestamp(0) NOT NULL,
	inserted_at timestamp(0) NOT NULL,
	CONSTRAINT subscription_pkey PRIMARY KEY (id)
);