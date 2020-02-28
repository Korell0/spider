DROP TABLE IF EXISTS spiders;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS spider_imgs;


CREATE TABLE spiders (
    id SERIAL PRIMARY KEY,
    spider_name VARCHAR NOT NULL,
    world VARCHAR(200),
    price INTEGER,
    information  TEXT

);


CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    user_name VARCHAR NOT NULL,
    hashed_password VARCHAR
);


CREATE TABLE orders (
    id SERIAL PRIMARY KEY NOT NULL,
    spider_id INTEGER NOT NULL,
    user_id INTEGER
);


CREATE TABLE spider_imgs (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    images TEXT
);