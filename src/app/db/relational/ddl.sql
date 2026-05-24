-- =============================================================================
-- PostgreSQL DDL: Normalized OLTP Schema in Third Normal Form (3NF)
-- Database: ecommerce_oltp
-- =============================================================================

-- Drop existing tables if they exist (for idempotent re-runs)
DROP TABLE IF EXISTS user_ratings CASCADE;
DROP TABLE IF EXISTS purchases CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- =============================================================================
-- 1. customers
-- PK: customer_id (SERIAL)
-- No repeating groups, no JSON/array columns.
-- All non-key columns depend only on customer_id (3NF).
-- =============================================================================
CREATE TABLE customers (
    customer_id    SERIAL        PRIMARY KEY,
    first_name     VARCHAR(100)  NOT NULL,
    last_name      VARCHAR(100)  NOT NULL,
    email          VARCHAR(255)  NOT NULL UNIQUE,
    phone          VARCHAR(50),
    address        TEXT,
    city           VARCHAR(100),
    state          VARCHAR(50),
    zip_code       VARCHAR(20),
    industry       VARCHAR(100),
    created_at     TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- Index on email for fast lookups
CREATE INDEX idx_customers_email ON customers (email);
-- Index on industry for targeted queries
CREATE INDEX idx_customers_industry ON customers (industry);

-- =============================================================================
-- 2. products
-- PK: product_id (SERIAL)
-- No repeating groups, no JSON/array columns.
-- Non-key columns (name, description, price, etc.) depend only on product_id.
-- =============================================================================
CREATE TABLE products (
    product_id      SERIAL        PRIMARY KEY,
    name            VARCHAR(255)  NOT NULL,
    description     TEXT,
    category        VARCHAR(100)  NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    stock_quantity  INTEGER       NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- Index on category for analytical queries
CREATE INDEX idx_products_category ON products (category);
-- Index on name for search
CREATE INDEX idx_products_name ON products (name);

-- =============================================================================
-- 3. purchases
-- PK: purchase_id (SERIAL)
-- FK: customer_id -> customers, product_id -> products
-- No repeating groups, no JSON/array columns.
-- Non-key columns (quantity, total_amount, etc.) depend only on purchase_id.
-- =============================================================================
CREATE TABLE purchases (
    purchase_id    SERIAL        PRIMARY KEY,
    customer_id    INTEGER       NOT NULL REFERENCES customers(customer_id),
    product_id     INTEGER       NOT NULL REFERENCES products(product_id),
    quantity       INTEGER       NOT NULL CHECK (quantity > 0),
    unit_price     NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    total_amount   NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
    purchase_date  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    payment_method VARCHAR(50)   NOT NULL DEFAULT 'credit_card'
);

-- Index on customer_id for "purchase history" queries
CREATE INDEX idx_purchases_customer ON purchases (customer_id);
-- Index on product_id for "product sales" queries
CREATE INDEX idx_purchases_product ON purchases (product_id);
-- Index on purchase_date for time-range queries
CREATE INDEX idx_purchases_date ON purchases (purchase_date);

-- =============================================================================
-- 4. user_ratings
-- PK: rating_id (SERIAL)
-- FK: customer_id -> customers, product_id -> products
-- No repeating groups, no JSON/array columns.
-- Non-key columns (rating, review_text) depend only on rating_id.
-- =============================================================================
CREATE TABLE user_ratings (
    rating_id    SERIAL        PRIMARY KEY,
    customer_id  INTEGER       NOT NULL REFERENCES customers(customer_id),
    product_id   INTEGER       NOT NULL REFERENCES products(product_id),
    rating       SMALLINT      NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text  TEXT,
    rating_date  TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- Index on product_id for "product ratings" queries
CREATE INDEX idx_ratings_product ON user_ratings (product_id);
-- Index on customer_id for "user reviews" queries
CREATE INDEX idx_ratings_customer ON user_ratings (customer_id);
-- Composite index for "ratings by product and rating score"
CREATE INDEX idx_ratings_product_score ON user_ratings (product_id, rating);
