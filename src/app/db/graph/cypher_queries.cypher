// =============================================================================
// Neo4j Cypher Scripts — Ecommerce Graph Schema
// =============================================================================

// ---------------------------------------------------------------------------
// 1. Create Nodes
// ---------------------------------------------------------------------------

// Customer nodes
CREATE (c1:Customer {
    customer_id: 1, first_name: 'Alice', last_name: 'Johnson',
    email: 'alice.johnson@email.com', industry: 'Technology'
});

CREATE (c2:Customer {
    customer_id: 2, first_name: 'Bob', last_name: 'Smith',
    email: 'bob.smith@email.com', industry: 'Finance'
});

CREATE (c3:Customer {
    customer_id: 3, first_name: 'Carol', last_name: 'Williams',
    email: 'carol.williams@email.com', industry: 'Healthcare'
});

// Product nodes
CREATE (p1:Product {
    product_id: 1, name: 'Ergonomic Office Chair',
    category: 'Furniture', unit_price: 299.99
});

CREATE (p2:Product {
    product_id: 2, name: 'Wireless Mechanical Keyboard',
    category: 'Electronics', unit_price: 149.99
});

CREATE (p3:Product {
    product_id: 3, name: '4K Monitor 27-inch',
    category: 'Electronics', unit_price: 499.99
});

CREATE (p4:Product {
    product_id: 4, name: 'Noise Cancelling Headphones',
    category: 'Electronics', unit_price: 249.99
});

CREATE (p5:Product {
    product_id: 5, name: 'Standing Desk Converter',
    category: 'Furniture', unit_price: 199.99
});

// Additional node type: Category
CREATE (cat1:Category {
    name: 'Electronics', description: 'Electronic devices and accessories'
});

CREATE (cat2:Category {
    name: 'Furniture', description: 'Office and home furniture'
});

// ---------------------------------------------------------------------------
// 2. Create Relationships
// ---------------------------------------------------------------------------

// PURCHASED: Customer -> Product
MATCH (c:Customer {customer_id: 1}), (p:Product {product_id: 1})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 299.99, date: '2024-01-15'}]->(p);

MATCH (c:Customer {customer_id: 1}), (p:Product {product_id: 2})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 149.99, date: '2024-01-15'}]->(p);

MATCH (c:Customer {customer_id: 2}), (p:Product {product_id: 3})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 499.99, date: '2024-01-22'}]->(p);

MATCH (c:Customer {customer_id: 2}), (p:Product {product_id: 5})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 199.99, date: '2024-01-22'}]->(p);

MATCH (c:Customer {customer_id: 3}), (p:Product {product_id: 4})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 249.99, date: '2024-02-01'}]->(p);

MATCH (c:Customer {customer_id: 3}), (p:Product {product_id: 3})
CREATE (c)-[:PURCHASED {quantity: 1, amount: 69.99, date: '2024-02-01'}]->(p);

// ALSO_BOUGHT: Product -> Product (collaborative filtering)
MATCH (p1:Product {product_id: 1}), (p2:Product {product_id: 2})
CREATE (p1)-[:ALSO_BOUGHT {strength: 0.8}]->(p2);

MATCH (p1:Product {product_id: 1}), (p2:Product {product_id: 5})
CREATE (p1)-[:ALSO_BOUGHT {strength: 0.6}]->(p2);

MATCH (p1:Product {product_id: 3}), (p2:Product {product_id: 5})
CREATE (p1)-[:ALSO_BOUGHT {strength: 0.7}]->(p2);

MATCH (p1:Product {product_id: 2}), (p2:Product {product_id: 3})
CREATE (p1)-[:ALSO_BOUGHT {strength: 0.9}]->(p2);

// BELONGS_TO: Product -> Category (additional relationship)
MATCH (p:Product), (c:Category) WHERE p.category = c.name
CREATE (p)-[:BELONGS_TO]->(c);

// ---------------------------------------------------------------------------
// 3. Recommendation Queries
// ---------------------------------------------------------------------------

// "Customers who bought X also bought Y"
MATCH (p1:Product {name: 'Ergonomic Office Chair'})<-[:PURCHASED]-()-[*..2]-(other:Product)
WHERE other <> p1
RETURN DISTINCT other.name AS recommended_product,
       other.category AS category,
       COUNT(*) AS score
ORDER BY score DESC;

// Top products by purchase count
MATCH (c:Customer)-[p:PURCHASED]->(prod:Product)
RETURN prod.name AS product_name, COUNT(*) AS purchase_count, SUM(p.amount) AS total_revenue
ORDER BY purchase_count DESC;

// Products in a category
MATCH (p:Product)-[:BELONGS_TO]->(c:Category {name: 'Electronics'})
RETURN p.name AS product_name, p.unit_price AS price
ORDER BY p.unit_price;

// Customer purchase history
MATCH (c:Customer {email: 'alice.johnson@email.com'})-[p:PURCHASED]->(prod:Product)
RETURN prod.name AS product_name, p.amount AS amount, p.date AS date
ORDER BY p.date DESC;
