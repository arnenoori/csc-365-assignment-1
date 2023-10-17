-- global_inventory table
create table
  public.global_inventory (
    id bigint generated always as identity primary key,
    created_at timestamp with time zone not null default now(),
    gold integer null default 100,
    num_red_ml integer null default 0,
    num_green_ml integer null default 0,
    num_blue_ml integer null default 0,
    num_dark_ml integer null default 0
  );

-- Version 3:

-- cart_items table
create table 
  public.cart_items (
    item_sku text,
    quantity integer,
    cart_id integer,
    constraint cart_items_fkey foreign key (cart_id) references carts(id)
  );

-- carts table
create table 
  public.carts (
    id bigint generated always as identity primary key,
    created_at timestamp with time zone not null default now(),
    customer text
  );

-- catalog table
create table 
  public.catalog (
    id bigint generated always as identity primary key,
    created_at timestamp with time zone not null default now(),
    sku text not null,
    name text not null,
    price bigint null,
    ml_per_barrel bigint null,
    num_red_ml bigint null,
    num_green_ml bigint null,
    num_blue_ml bigint null,
    num_dark_ml bigint null,
    quantity bigint null
  );

-- deliveries table
create table 
  public.deliveries (
    id bigint generated always as identity primary key,
    created_at timestamp with time zone not null default now(),
    catalog_id bigint not null,
    quantity bigint not null,
    foreign key (catalog_id) references catalog(id)
  );

-- Version 4:

-- inventory_transactions table
create table 
  public.inventory_transactions (
    id bigint generated always as identity primary key,
    created_at timestamp with time zone not null default current_timestamp,
    description text
  );

-- inventory_ledger_entries table
create table 
  public.inventory_ledger_entries (
    id bigint generated always as identity primary key,
    inventory_id integer,
    transaction_id integer,
    change integer,
    foreign key (inventory_id) references global_inventory (id),
    foreign key (transaction_id) references inventory_transactions (id)
  );

-- Adding a foreign key to the global_inventory table
alter table 
  public.global_inventory
add foreign key (potion_id) references potions(id);
