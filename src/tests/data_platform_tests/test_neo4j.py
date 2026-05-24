"""Tests for Neo4j graph model (nodes, relationships, recommendation queries)."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from neo4j import AsyncGraphDatabase

from src.app.routers.graph.category.repositories.category_repo import (
    CategoryRepo,
)
from src.app.routers.graph.customer.repositories.customer_repo import (
    CustomerRepo,
)
from src.app.routers.graph.init_db.repositories.init_db_repo import (
    InitDBRepo,
)
from src.app.routers.graph.product.repositories.product_repo import (
    ProductRepo,
)


async def _async_iter(*items: Any) -> Any:
    for item in items:
        yield item


GRAPH_SEED_STATEMENTS: list[str] = [
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


@pytest.fixture
def init_repo() -> InitDBRepo:
    return InitDBRepo()


@pytest.fixture
def customer_repo() -> CustomerRepo:
    return CustomerRepo()


@pytest.fixture
def product_repo() -> ProductRepo:
    return ProductRepo()


@pytest.fixture
def category_repo() -> CategoryRepo:
    return CategoryRepo()


class TestNeo4jGraphSchema:
    def test_repo_exists(self) -> None:
        repo = InitDBRepo()
        assert hasattr(repo, "create_graph_schema")

    @pytest.mark.asyncio
    async def test_create_graph_schema_invokes_cypher(
        self, init_repo: InitDBRepo
    ) -> None:
        mock_driver = MagicMock()
        mock_session = AsyncMock()
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_session.run = AsyncMock(return_value=mock_result)
        mock_result.data = MagicMock(return_value=[])

        await init_repo.create_graph_schema(mock_driver, GRAPH_SEED_STATEMENTS)

        expected_calls = 1 + len(GRAPH_SEED_STATEMENTS)  # DETACH DELETE + all statements
        assert mock_session.run.call_count == expected_calls, (
            f"Expected {expected_calls} Cypher calls, got {mock_session.run.call_count}"
        )

    def test_get_driver_creates_connection(self) -> None:
        driver = AsyncGraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password"),
        )
        assert driver is not None


class TestNeo4jQueries:
    @pytest.mark.asyncio
    async def test_also_bought_recommendation_pattern(
        self, product_repo: ProductRepo
    ) -> None:
        mock_driver = MagicMock()
        mock_session = AsyncMock()
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.__aiter__ = lambda _: _async_iter(
            {"product_name": "Mouse", "recommendation_score": 5}
        )
        mock_session.run = AsyncMock(return_value=mock_result)

        results = await product_repo.get_also_bought_recommendations(
            mock_driver, "Keyboard", 5
        )
        assert len(results) == 1
        assert results[0]["product_name"] == "Mouse"

    @pytest.mark.asyncio
    async def test_customer_purchase_history(
        self, customer_repo: CustomerRepo
    ) -> None:
        mock_driver = MagicMock()
        mock_session = AsyncMock()
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.__aiter__ = lambda _: _async_iter(
            {"product_name": "Keyboard", "category": "Electronics"}
        )
        mock_session.run = AsyncMock(return_value=mock_result)

        results = await customer_repo.get_purchase_history(
            mock_driver, "alice@example.com"
        )
        assert len(results) == 1
        assert results[0]["product_name"] == "Keyboard"

    @pytest.mark.asyncio
    async def test_products_by_category_recommendation(
        self, category_repo: CategoryRepo
    ) -> None:
        mock_driver = MagicMock()
        mock_session = AsyncMock()
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.__aiter__ = lambda _: _async_iter(
            {"product_name": "Monitor", "product_id": 3}
        )
        mock_session.run = AsyncMock(return_value=mock_result)

        results = await category_repo.get_products_by_category(
            mock_driver, "Electronics"
        )
        assert len(results) == 1
        assert results[0]["product_name"] == "Monitor"

    @pytest.mark.asyncio
    async def test_top_products_overall(
        self, product_repo: ProductRepo
    ) -> None:
        mock_driver = MagicMock()
        mock_session = AsyncMock()
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        mock_result = MagicMock()
        mock_result.__aiter__ = lambda _: _async_iter(
            {"product_name": "Mouse", "purchase_count": 10}
        )
        mock_session.run = AsyncMock(return_value=mock_result)

        results = await product_repo.get_top_products(mock_driver, 5)
        assert len(results) == 1
        assert results[0]["product_name"] == "Mouse"

