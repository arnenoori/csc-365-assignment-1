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

-- initial game state:

INSERT INTO global_inventory (gold, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml)
VALUES (100, 0, 0, 0, 0);

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
create table public.catalog (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    sku TEXT NOT NULL,
    name TEXT NOT NULL,
    price BIGINT NOT NULL CHECK (price BETWEEN 1 AND 500),
    ml_per_barrel BIGINT NOT NULL,
    num_red_ml BIGINT NOT NULL,
    num_green_ml BIGINT NOT NULL,
    num_blue_ml BIGINT NOT NULL,
    num_dark_ml BIGINT NOT NULL,
    quantity BIGINT NOT NULL CHECK (quantity BETWEEN 0 AND 10000),
    CHECK ((num_red_ml + num_green_ml + num_blue_ml + num_dark_ml) = 100)
);

INSERT INTO public.catalog (sku, name, price, num_red_ml, num_green_ml, num_blue_ml, num_dark_ml, ml_per_barrel, quantity)
VALUES 
  ('SKU1', 'Pure Red Potion', 100, 100, 0, 0, 0, 100, 0),
  ('SKU2', 'Pure Green Potion', 100, 0, 100, 0, 0, 100, 0),
  ('SKU3', 'Pure Blue Potion', 100, 0, 0, 100, 0, 100, 0),
  ('SKU5', 'Purple Potion', 25, 50, 0, 50, 0, 100, 0),
  ('SKU6', 'Cyan Potion', 25, 0, 50, 50, 0, 100, 0),
  ('SKU8', 'Yellow Potion', 25, 50, 50, 0, 0, 100, 0),

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
    inventory_type varchar(255),
    transaction_id integer,
    change integer,
    foreign key (transaction_id) references inventory_transactions (id)
  );


-- Version 5:

  -- Dummy customers

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Scaramouche')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  '1 oblivion potion', 
  50, 
  id AS cart_id
FROM 
  inserted;

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Cellar')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  'Pure Green Potion', 
  70, 
  id AS cart_id
FROM 
  inserted;

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Barlan')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  'Cyan Potion', 
  41, 
  id AS cart_id
FROM 
  inserted;

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Dellen')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  'Yellow Potion', 
  21, 
  id AS cart_id
FROM 
  inserted;

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Daedor')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  'Cyan Potion', 
  166, 
  id AS cart_id
FROM 
  inserted;

WITH inserted AS (
  INSERT INTO carts (customer)
  VALUES 
    ('Snow')
  RETURNING id
)
INSERT INTO cart_items (item_sku, quantity, cart_id)
SELECT 
  'Purple Potion', 
  250, 
  id AS cart_id
FROM 
  inserted; 