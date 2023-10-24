--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.4 (Ubuntu 15.4-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: key; Type: TABLE DATA; Schema: pgsodium; Owner: supabase_admin
--



--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: catalog; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."catalog" ("id", "created_at", "sku", "name", "price", "ml_per_barrel", "num_red_ml", "num_green_ml", "num_blue_ml", "num_dark_ml", "quantity") OVERRIDING SYSTEM VALUE VALUES
	(29, '2023-10-18 20:22:21.954264+00', 'SKU2', 'Pure Green Potion', 100, 100, 0, 100, 0, 0, 0),
	(30, '2023-10-18 20:22:21.954264+00', 'SKU3', 'Pure Blue Potion', 100, 100, 0, 0, 100, 0, 0),
	(32, '2023-10-18 20:22:21.954264+00', 'SKU5', 'Purple Potion', 25, 100, 50, 0, 50, 0, 0),
	(33, '2023-10-18 20:22:21.954264+00', 'SKU6', 'Cyan Potion', 25, 100, 0, 50, 50, 0, 0),
	(35, '2023-10-18 20:22:21.954264+00', 'SKU8', 'Yellow Potion', 25, 100, 50, 50, 0, 0, 0),
	(28, '2023-10-18 20:22:21.954264+00', 'SKU1', 'Pure Red Potion', 100, 100, 100, 0, 0, 0, 10);


--
-- Data for Name: deliveries; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: global_inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."global_inventory" ("id", "created_at", "gold", "num_red_ml", "num_green_ml", "num_blue_ml", "num_dark_ml") OVERRIDING SYSTEM VALUE VALUES
	(1, '2023-10-17 16:09:51.606276+00', 0, 0, 0, 0, 0);


--
-- Data for Name: inventory_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: inventory_ledger_entries; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1, false);


--
-- Name: key_key_id_seq; Type: SEQUENCE SET; Schema: pgsodium; Owner: supabase_admin
--

SELECT pg_catalog.setval('"pgsodium"."key_key_id_seq"', 1, false);


--
-- Name: carts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."carts_id_seq"', 6, true);


--
-- Name: catalog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."catalog_id_seq"', 36, true);


--
-- Name: deliveries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."deliveries_id_seq"', 1, false);


--
-- Name: global_inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."global_inventory_id_seq"', 1, true);


--
-- Name: inventory_ledger_entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."inventory_ledger_entries_id_seq"', 1, false);


--
-- Name: inventory_transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."inventory_transactions_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

RESET ALL;
