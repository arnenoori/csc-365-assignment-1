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
