
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

CREATE EXTENSION IF NOT EXISTS "pg_cron" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pg_net" WITH SCHEMA "public";

CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";

CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";

CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";

CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";

SET default_tablespace = '';

SET default_table_access_method = "heap";

CREATE TABLE IF NOT EXISTS "public"."cart_items" (
    "item_sku" "text",
    "quantity" integer,
    "cart_id" integer
);

ALTER TABLE "public"."cart_items" OWNER TO "postgres";

CREATE TABLE IF NOT EXISTS "public"."carts" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "customer" "text"
);

ALTER TABLE "public"."carts" OWNER TO "postgres";

ALTER TABLE "public"."carts" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."carts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."catalog" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "sku" "text" NOT NULL,
    "name" "text" NOT NULL,
    "price" bigint NOT NULL,
    "ml_per_barrel" bigint NOT NULL,
    "num_red_ml" bigint NOT NULL,
    "num_green_ml" bigint NOT NULL,
    "num_blue_ml" bigint NOT NULL,
    "num_dark_ml" bigint NOT NULL,
    "quantity" bigint NOT NULL,
    CONSTRAINT "catalog_check" CHECK ((((("num_red_ml" + "num_green_ml") + "num_blue_ml") + "num_dark_ml") = 100)),
    CONSTRAINT "catalog_price_check" CHECK ((("price" >= 1) AND ("price" <= 500))),
    CONSTRAINT "catalog_quantity_check" CHECK ((("quantity" >= 0) AND ("quantity" <= 10000)))
);

ALTER TABLE "public"."catalog" OWNER TO "postgres";

ALTER TABLE "public"."catalog" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."catalog_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."deliveries" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "catalog_id" bigint NOT NULL,
    "quantity" bigint NOT NULL
);

ALTER TABLE "public"."deliveries" OWNER TO "postgres";

ALTER TABLE "public"."deliveries" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."deliveries_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."global_inventory" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "gold" integer DEFAULT 100,
    "num_red_ml" integer DEFAULT 0,
    "num_green_ml" integer DEFAULT 0,
    "num_blue_ml" integer DEFAULT 0,
    "num_dark_ml" integer DEFAULT 0
);

ALTER TABLE "public"."global_inventory" OWNER TO "postgres";

ALTER TABLE "public"."global_inventory" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."global_inventory_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."inventory_ledger_entries" (
    "id" bigint NOT NULL,
    "inventory_id" integer,
    "transaction_id" integer,
    "change" integer
);

ALTER TABLE "public"."inventory_ledger_entries" OWNER TO "postgres";

ALTER TABLE "public"."inventory_ledger_entries" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."inventory_ledger_entries_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE IF NOT EXISTS "public"."inventory_transactions" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "description" "text"
);

ALTER TABLE "public"."inventory_transactions" OWNER TO "postgres";

ALTER TABLE "public"."inventory_transactions" ALTER COLUMN "id" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME "public"."inventory_transactions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY "public"."carts"
    ADD CONSTRAINT "carts_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."catalog"
    ADD CONSTRAINT "catalog_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."deliveries"
    ADD CONSTRAINT "deliveries_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."global_inventory"
    ADD CONSTRAINT "global_inventory_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."inventory_ledger_entries"
    ADD CONSTRAINT "inventory_ledger_entries_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."inventory_transactions"
    ADD CONSTRAINT "inventory_transactions_pkey" PRIMARY KEY ("id");

ALTER TABLE ONLY "public"."cart_items"
    ADD CONSTRAINT "cart_items_fkey" FOREIGN KEY ("cart_id") REFERENCES "public"."carts"("id");

ALTER TABLE ONLY "public"."inventory_ledger_entries"
    ADD CONSTRAINT "inventory_ledger_entries_inventory_id_fkey" FOREIGN KEY ("inventory_id") REFERENCES "public"."global_inventory"("id");

ALTER TABLE ONLY "public"."inventory_ledger_entries"
    ADD CONSTRAINT "inventory_ledger_entries_transaction_id_fkey" FOREIGN KEY ("transaction_id") REFERENCES "public"."inventory_transactions"("id");

GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

GRANT ALL ON TABLE "public"."cart_items" TO "anon";
GRANT ALL ON TABLE "public"."cart_items" TO "authenticated";
GRANT ALL ON TABLE "public"."cart_items" TO "service_role";

GRANT ALL ON TABLE "public"."carts" TO "anon";
GRANT ALL ON TABLE "public"."carts" TO "authenticated";
GRANT ALL ON TABLE "public"."carts" TO "service_role";

GRANT ALL ON SEQUENCE "public"."carts_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."carts_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."carts_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."catalog" TO "anon";
GRANT ALL ON TABLE "public"."catalog" TO "authenticated";
GRANT ALL ON TABLE "public"."catalog" TO "service_role";

GRANT ALL ON SEQUENCE "public"."catalog_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."catalog_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."catalog_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."deliveries" TO "anon";
GRANT ALL ON TABLE "public"."deliveries" TO "authenticated";
GRANT ALL ON TABLE "public"."deliveries" TO "service_role";

GRANT ALL ON SEQUENCE "public"."deliveries_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."deliveries_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."deliveries_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."global_inventory" TO "anon";
GRANT ALL ON TABLE "public"."global_inventory" TO "authenticated";
GRANT ALL ON TABLE "public"."global_inventory" TO "service_role";

GRANT ALL ON SEQUENCE "public"."global_inventory_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."global_inventory_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."global_inventory_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."inventory_ledger_entries" TO "anon";
GRANT ALL ON TABLE "public"."inventory_ledger_entries" TO "authenticated";
GRANT ALL ON TABLE "public"."inventory_ledger_entries" TO "service_role";

GRANT ALL ON SEQUENCE "public"."inventory_ledger_entries_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."inventory_ledger_entries_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."inventory_ledger_entries_id_seq" TO "service_role";

GRANT ALL ON TABLE "public"."inventory_transactions" TO "anon";
GRANT ALL ON TABLE "public"."inventory_transactions" TO "authenticated";
GRANT ALL ON TABLE "public"."inventory_transactions" TO "service_role";

GRANT ALL ON SEQUENCE "public"."inventory_transactions_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."inventory_transactions_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."inventory_transactions_id_seq" TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";

ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";

RESET ALL;
