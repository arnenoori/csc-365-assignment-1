-- global_inventory table
CREATE TABLE public.global_inventory (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    gold INTEGER NULL DEFAULT 100,
    num_red_ml INTEGER NULL DEFAULT 0,
    num_green_ml INTEGER NULL DEFAULT 0,
    num_blue_ml INTEGER NULL DEFAULT 0,
    num_dark_ml INTEGER NULL DEFAULT 0
)

-- cart_items table
CREATE TABLE cart_items (
    item_sku TEXT,
    quantity INT,
    cart_id INT,
    CONSTRAINT cart_items_fkey FOREIGN KEY (cart_id) REFERENCES carts(id)
);

-- carts table
CREATE TABLE carts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    customer TEXT
);

-- catalog table
CREATE TABLE public.catalog (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    sku TEXT NOT NULL,
    name TEXT NOT NULL,
    price BIGINT NULL,
    num_red_ml BIGINT NULL,
    num_green_ml BIGINT NULL,
    num_blue_ml BIGINT NULL,
    num_dark_ml BIGINT NULL,
    quantity BIGINT NULL
)

-- inventory_transactions table
CREATE TABLE inventory_transactions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    description TEXT
);

-- inventory_ledger_entries table
CREATE TABLE inventory_ledger_entries (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inventory_id INT,
    transaction_id INT,
    change INT,
    FOREIGN KEY (inventory_id) REFERENCES global_inventory (id),
    FOREIGN KEY (transaction_id) REFERENCES inventory_transactions (id)
);

-- Adding a foreign key to the global_inventory table
ALTER TABLE global_inventory
ADD FOREIGN KEY (potion_id) REFERENCES potions(id);