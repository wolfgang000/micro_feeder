CREATE TABLE public.subscription (
	id bigserial NOT NULL,
	webhook_url text NOT NULL,
	feed_url text NOT NULL,
	CONSTRAINT subscription_pkey PRIMARY KEY (id)
);