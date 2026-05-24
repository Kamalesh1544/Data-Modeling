"""
Initialize all three databases (PostgreSQL, MongoDB, Neo4j) with schemas and seed data.

Usage:
    python scripts/init_databases.py [--pg-only] [--mongo-only] [--neo4j-only]
"""

from __future__ import annotations

import asyncio
import sys
from datetime import UTC, datetime
from typing import Any

from bson.objectid import ObjectId

from src.app.core import logger


PRODUCT_SEED: list[dict[str, Any]] = [
    {
        "name": "Ergonomic Office Chair",
        "description": "High-back mesh office chair with lumbar support",
        "category": "Furniture",
        "unit_price": 299.99,
        "stock_quantity": 50,
        "material": "Mesh",
        "color": "Black",
        "warranty_years": 5,
        "created_at": datetime.now(UTC),
    },
    {
        "name": "Wireless Mechanical Keyboard",
        "description": "RGB backlit wireless mechanical keyboard",
        "category": "Electronics",
        "unit_price": 149.99,
        "stock_quantity": 120,
        "switch_type": "Cherry MX Blue",
        "backlight": "RGB",
        "wireless": True,
        "battery_life_hours": 40,
        "created_at": datetime.now(UTC),
    },
    {
        "name": "4K Monitor 27-inch",
        "description": "27-inch IPS 4K UHD monitor with USB-C",
        "category": "Electronics",
        "unit_price": 499.99,
        "stock_quantity": 30,
        "resolution": "3840x2160",
        "panel_type": "IPS",
        "refresh_rate_hz": 60,
        "ports": ["HDMI", "DisplayPort", "USB-C"],
        "created_at": datetime.now(UTC),
    },
    {
        "name": "Noise Cancelling Headphones",
        "description": "Over-ear Bluetooth headphones with ANC",
        "category": "Electronics",
        "unit_price": 249.99,
        "stock_quantity": 45,
        "driver_size_mm": 40,
        "battery_life_hours": 30,
        "foldable": True,
        "created_at": datetime.now(UTC),
    },
    {
        "name": "Desk LED Lamp",
        "description": "LED desk lamp with adjustable brightness",
        "category": "Lighting",
        "unit_price": 45.99,
        "stock_quantity": 90,
        "brightness_levels": 5,
        "color_temperature": "3000K-6500K",
        "usb_charging": True,
        "created_at": datetime.now(UTC),
    },
]


def _rp(pid: str, name: str, amt: float, y: int, m: int, d: int, h: int, mi: int) -> dict[str, Any]:
    return {
        "product_id": pid,
        "product_name": name,
        "amount": amt,
        "date": datetime(y, m, d, h, mi),
    }


def _mp(pid: str, name: str, reason: str) -> dict[str, Any]:
    return {"product_id": pid, "product_name": name, "reason": reason}


def _build_customers(pids: list[ObjectId]) -> list[dict[str, Any]]:
    return [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@email.com",
            "industry": "Technology",
            "recent_purchases": [
                _rp(str(pids[0]), "Ergonomic Office Chair", 299.99, 2024, 1, 15, 10, 30),
                _rp(str(pids[1]), "Wireless Mechanical Keyboard", 149.99, 2024, 1, 15, 10, 30),
                _rp(str(pids[2]), "4K Monitor 27-inch", 499.99, 2024, 2, 20, 14, 15),
            ],
            "matched_products": [
                _mp(str(pids[1]), "Wireless Mechanical Keyboard", "Technology industry match"),
                _mp(str(pids[2]), "4K Monitor 27-inch", "Technology industry match"),
            ],
            "created_at": datetime.now(UTC),
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@email.com",
            "industry": "Finance",
            "recent_purchases": [
                _rp(str(pids[0]), "Ergonomic Office Chair", 199.99, 2024, 1, 22, 9, 0),
                _rp(str(pids[4]), "Standing Desk Converter", 499.99, 2024, 1, 22, 9, 0),
            ],
            "matched_products": [
                _mp(str(pids[2]), "4K Monitor 27-inch", "Finance industry - analytical work"),
            ],
            "created_at": datetime.now(UTC),
        },
        {
            "first_name": "Carol",
            "last_name": "Williams",
            "email": "carol.williams@email.com",
            "industry": "Healthcare",
            "recent_purchases": [
                _rp(str(pids[3]), "Noise Cancelling Headphones", 249.99, 2024, 2, 1, 16, 0),
                _rp(str(pids[2]), "4K Monitor 27-inch", 69.99, 2024, 2, 1, 16, 0),
            ],
            "matched_products": [
                _mp(str(pids[3]), "Noise Cancelling Headphones",
                    "Healthcare - focus in noisy env"),
            ],
            "created_at": datetime.now(UTC),
        },
    ]


def _build_purchases(cids: list[ObjectId], pids: list[ObjectId]) -> list[dict[str, Any]]:
    return [
        {
            "customer_id": str(cids[0]), "product_id": str(pids[0]),
            "quantity": 1, "total_amount": 299.99,
            "purchase_date": datetime(2024, 1, 15, 10, 30),
            "payment_method": "credit_card",
        },
        {
            "customer_id": str(cids[0]), "product_id": str(pids[1]),
            "quantity": 1, "total_amount": 149.99,
            "purchase_date": datetime(2024, 1, 15, 10, 30),
            "payment_method": "credit_card",
        },
        {
            "customer_id": str(cids[1]), "product_id": str(pids[2]),
            "quantity": 1, "total_amount": 499.99,
            "purchase_date": datetime(2024, 1, 22, 9, 0),
            "payment_method": "debit_card",
        },
        {
            "customer_id": str(cids[2]), "product_id": str(pids[3]),
            "quantity": 1, "total_amount": 249.99,
            "purchase_date": datetime(2024, 2, 1, 16, 0),
            "payment_method": "credit_card",
        },
    ]


GRAPH_CYPHER_STATEMENTS: list[str] = [
    (
        "CREATE (c1:Customer {customer_id: 1, first_name: 'Alice',"
        " last_name: 'Johnson', email: 'alice.johnson@email.com', industry: 'Technology'})"
    ),
    (
        "CREATE (c2:Customer {customer_id: 2, first_name: 'Bob',"
        " last_name: 'Smith', email: 'bob.smith@email.com', industry: 'Finance'})"
    ),
    (
        "CREATE (c3:Customer {customer_id: 3, first_name: 'Carol',"
        " last_name: 'Williams', email: 'carol.williams@email.com', industry: 'Healthcare'})"
    ),
    (
        "CREATE (p1:Product {product_id: 1, name: 'Ergonomic Office Chair',"
        " category: 'Furniture', unit_price: 299.99})"
    ),
    (
        "CREATE (p2:Product {product_id: 2, name: 'Wireless Mechanical Keyboard',"
        " category: 'Electronics', unit_price: 149.99})"
    ),
    (
        "CREATE (p3:Product {product_id: 3, name: '4K Monitor 27-inch',"
        " category: 'Electronics', unit_price: 499.99})"
    ),
    (
        "CREATE (p4:Product {product_id: 4, name: 'Noise Cancelling Headphones',"
        " category: 'Electronics', unit_price: 249.99})"
    ),
    (
        "CREATE (p5:Product {product_id: 5, name: 'Standing Desk Converter',"
        " category: 'Furniture', unit_price: 199.99})"
    ),
    (
        "CREATE (cat1:Category {name: 'Electronics',"
        " description: 'Electronic devices and accessories'})"
    ),
    (
        "CREATE (cat2:Category {name: 'Furniture',"
        " description: 'Office and home furniture'})"
    ),
    (
        "MATCH (c:Customer {customer_id: 1}), (p:Product {product_id: 1})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 299.99, date: '2024-01-15'}]->(p)"
    ),
    (
        "MATCH (c:Customer {customer_id: 1}), (p:Product {product_id: 2})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 149.99, date: '2024-01-15'}]->(p)"
    ),
    (
        "MATCH (c:Customer {customer_id: 2}), (p:Product {product_id: 3})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 499.99, date: '2024-01-22'}]->(p)"
    ),
    (
        "MATCH (c:Customer {customer_id: 2}), (p:Product {product_id: 5})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 199.99, date: '2024-01-22'}]->(p)"
    ),
    (
        "MATCH (c:Customer {customer_id: 3}), (p:Product {product_id: 4})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 249.99, date: '2024-02-01'}]->(p)"
    ),
    (
        "MATCH (c:Customer {customer_id: 3}), (p:Product {product_id: 3})"
        " CREATE (c)-[:PURCHASED {quantity: 1, amount: 69.99, date: '2024-02-01'}]->(p)"
    ),
    (
        "MATCH (p1:Product {product_id: 1}), (p2:Product {product_id: 2})"
        " CREATE (p1)-[:ALSO_BOUGHT {strength: 0.8}]->(p2)"
    ),
    (
        "MATCH (p1:Product {product_id: 1}), (p2:Product {product_id: 5})"
        " CREATE (p1)-[:ALSO_BOUGHT {strength: 0.6}]->(p2)"
    ),
    (
        "MATCH (p1:Product {product_id: 3}), (p2:Product {product_id: 5})"
        " CREATE (p1)-[:ALSO_BOUGHT {strength: 0.7}]->(p2)"
    ),
    (
        "MATCH (p1:Product {product_id: 2}), (p2:Product {product_id: 3})"
        " CREATE (p1)-[:ALSO_BOUGHT {strength: 0.9}]->(p2)"
    ),
    "MATCH (p:Product), (c:Category) WHERE p.category = c.name CREATE (p)-[:BELONGS_TO]->(c)",
]


async def init_postgres() -> dict[str, int]:
    from src.app.routers.relational.init_db.repositories.init_db_repo import (
        InitDBRepo,
    )
    from src.app.routers.relational.init_db.services.init_db_service import (
        InitDBService,
    )

    logger.info("=== Initializing PostgreSQL ===")
    service = InitDBService(init_db_repo=InitDBRepo())
    counts = await service.init_database()
    logger.info("PostgreSQL seeded: %s", counts)
    return counts


async def init_mongodb() -> dict[str, int]:
    from src.app.routers.document.customer.repositories.customer_repo import (
        CustomerRepo,
    )
    from src.app.routers.document.init_db.repositories.init_db_repo import (
        InitDBRepo,
    )
    from src.app.routers.document.init_db.services.init_db_service import (
        InitDBService,
    )
    from src.app.routers.document.product.repositories.product_repo import (
        ProductRepo,
    )
    from src.app.routers.document.purchase.repositories.purchase_repo import (
        PurchaseRepo,
    )

    logger.info("=== Initializing MongoDB ===")
    service = InitDBService(
        init_db_repo=InitDBRepo(),
        product_repo=ProductRepo(),
        customer_repo=CustomerRepo(),
        purchase_repo=PurchaseRepo(),
    )
    placeholder_ids = [ObjectId() for _ in range(5)]
    counts = await service.init_database(
        products=PRODUCT_SEED,
        customers=_build_customers(placeholder_ids),
        purchases=_build_purchases(
            [ObjectId() for _ in range(3)],
            placeholder_ids,
        ),
    )
    logger.info("MongoDB seeded: %s", counts)
    return counts


async def init_neo4j() -> dict[str, str]:
    from src.app.routers.graph.init_db.repositories.init_db_repo import (
        InitDBRepo,
    )
    from src.app.routers.graph.init_db.services.init_db_service import (
        InitDBService,
    )

    logger.info("=== Initializing Neo4j ===")
    service = InitDBService(init_db_repo=InitDBRepo())
    result = await service.init_database(cypher_statements=GRAPH_CYPHER_STATEMENTS)
    logger.info("Neo4j graph schema created")
    return result


async def main() -> None:
    flags = set(sys.argv[1:]) if len(sys.argv) > 1 else set()

    run_all = not flags or "--all" in flags
    run_pg = run_all or "--pg-only" in flags
    run_mongo = run_all or "--mongo-only" in flags
    run_neo4j = run_all or "--neo4j-only" in flags

    results: dict[str, object] = {}

    if run_pg:
        results["postgres"] = await init_postgres()
    if run_mongo:
        results["mongodb"] = await init_mongodb()
    if run_neo4j:
        results["neo4j"] = await init_neo4j()

    logger.info("=== Initialization complete ===")
    logger.info("%s", results)


if __name__ == "__main__":
    asyncio.run(main())

