CREATE TABLE global_inventory (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    gold INT,
    potion_id INT,
    quantity INT,
    ml INT,
    price INT
);

CREATE TABLE potions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    potion_type INT,
    price INT,
    quantity INT
);

CREATE TABLE cart_items (
    item_sku VARCHAR(255),
    quantity INT,
    card_id INT
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    customer VARCHAR(255)
);

ALTER TABLE global_inventory
ADD FOREIGN KEY (potion_id) REFERENCES potions(id);

-- Version 4:

create table
  inventory_transactions (
    id SERIAL primary key,
    created_at timestamp default current_timestamp,
    description varchar(255)
  );

create table
  inventory_ledger_entries (
    id SERIAL primary key,
    inventory_id int,
    transaction_id int,
    change int,
    foreign key (inventory_id) references global_inventory (id),
    foreign key (transaction_id) references inventory_transactions (id)
  );