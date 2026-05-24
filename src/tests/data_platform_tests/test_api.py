"""API integration tests for data platform endpoints (relational, document, graph)."""

from __future__ import annotations

import sys
from unittest.mock import AsyncMock, MagicMock

import pytest


# ---------------------------------------------------------------------------
# Patch external modules BEFORE any app imports
# ---------------------------------------------------------------------------
firebase_admin_mod = MagicMock()
firebase_admin_mod.credentials = MagicMock()
firebase_admin_mod.initialize_app = MagicMock()
firebase_admin_mod.auth = MagicMock()
firebase_admin_mod.auth.verify_id_token = MagicMock(return_value={"uid": "1234"})

import types


snowflakekit_mod = types.ModuleType("snowflakekit")
snowflakekit_mod.SnowflakeConfig = MagicMock
snowflakekit_mod.SnowflakeGenerator = MagicMock

aioredis_mod = types.ModuleType("aioredis")
aioredis_mod.from_url = MagicMock()

sys.modules["firebase_admin"] = firebase_admin_mod
sys.modules["firebase_admin.auth"] = firebase_admin_mod.auth
sys.modules["firebase_admin.credentials"] = firebase_admin_mod.credentials
sys.modules["snowflakekit"] = snowflakekit_mod
sys.modules["aioredis"] = aioredis_mod

# ---------------------------------------------------------------------------
# Patch database init functions before main.py calls setup_db(app)
# ---------------------------------------------------------------------------
import src.app.db.setup_database as _setup_db_mod


async def _noop_init():
    pass

_setup_db_mod._init_relational_schema = _noop_init
_setup_db_mod._init_document_schema = _noop_init

# ---------------------------------------------------------------------------
# Make UserTable accessible from src.app.db before auth router imports it
# ---------------------------------------------------------------------------
import src.app.db as _app_db
from src.app.db.tables import user_tables as _user_tables


_app_db.UserTable = _user_tables.UserTable
_app_db.TORTOISE_ORM = _setup_db_mod.TORTOISE_ORM

# ---------------------------------------------------------------------------
# Now safe to import the app
# ---------------------------------------------------------------------------
from fastapi.testclient import TestClient

from src.app.core.auth import get_current_user
from src.app.main import app
from src.app.utils.schemas.user_schemas import AuthUserSchema


def _fake_user() -> AuthUserSchema:
    return AuthUserSchema(
        name="Test User",
        role="admin",
        company=1,
        uuid="1234",
        user_id="1234",
        email="test@example.com",
        email_verified=True,
        firebase={},
        uid="1234",
    )


app.dependency_overrides[get_current_user] = lambda: _fake_user()
client = TestClient(app)

from src.app.core.di import container


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _mock_all_services():
    from src.app.routers.document.customer.services.customer_service import (
        CustomerService as DocCustomerService,
    )
    from src.app.routers.document.init_db.services.init_db_service import (
        InitDBService as DocInitDBService,
    )
    from src.app.routers.document.product.services.product_service import (
        ProductService as DocProductService,
    )
    from src.app.routers.document.purchase.services.purchase_service import (
        PurchaseService as DocPurchaseService,
    )
    from src.app.routers.graph.category.services.category_service import (
        CategoryService,
    )
    from src.app.routers.graph.customer.services.customer_service import (
        CustomerService as GraphCustomerService,
    )
    from src.app.routers.graph.init_db.services.init_db_service import (
        InitDBService as GraphInitDBService,
    )
    from src.app.routers.graph.product.services.product_service import (
        ProductService as GraphProductService,
    )
    from src.app.routers.relational.customer.services.customer_service import (
        CustomerService as RelCustomerService,
    )
    from src.app.routers.relational.init_db.services.init_db_service import (
        InitDBService as RelInitDBService,
    )
    from src.app.routers.relational.product.services.product_service import (
        ProductService as RelProductService,
    )

    mocks = {
        RelCustomerService: "get_customers_with_purchases",
        RelInitDBService: "init_database",
        RelProductService: ("get_top_products", "get_product_recommendations"),
        DocCustomerService: "get_customers_with_embeddings",
        DocInitDBService: "init_database",
        DocProductService: "get_products_by_category",
        DocPurchaseService: "get_purchases_by_customer",
        CategoryService: "get_products_by_category",
        GraphCustomerService: "get_purchase_history",
        GraphInitDBService: "init_database",
        GraphProductService: ("get_also_bought_recommendations", "get_top_products"),
    }

    for svc_cls, methods in mocks.items():
        instance = container.get(svc_cls)
        if isinstance(methods, str):
            setattr(instance, methods, AsyncMock(return_value=[]))
        else:
            for m in methods:
                setattr(instance, m, AsyncMock(return_value=[]))

    yield


# ---------------------------------------------------------------------------
# Relational API tests
# ---------------------------------------------------------------------------

class TestRelationalAPI:
    def test_init_postgres(self):
        from src.app.routers.relational.init_db.services.init_db_service import (
            InitDBService,
        )

        container.get(InitDBService).init_database = AsyncMock(
            return_value={"customers": 4, "products": 5, "purchases": 4, "user_ratings": 3}
        )
        resp = client.post("/api/oltp/init")
        assert resp.status_code == 200
        data = resp.json()
        assert "tables_seeded" in data
        assert data["tables_seeded"]["customers"] == 4

    def test_customers_with_purchases(self):
        from src.app.routers.relational.customer.services.customer_service import (
            CustomerService,
        )

        container.get(CustomerService).get_customers_with_purchases = AsyncMock(
            return_value=[
                {
                    "customer_id": 1,
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "email": "alice@example.com",
                    "industry": "Technology",
                    "purchase_id": 10,
                    "product_id": 5,
                    "product_name": "Keyboard",
                    "quantity": 1,
                    "total_amount": "149.99",
                    "purchase_date": "2024-01-15T10:30:00Z",
                }
            ]
        )
        resp = client.get("/api/oltp/customers-with-purchases?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["first_name"] == "Alice"

    def test_top_products_relational(self):
        from src.app.routers.relational.product.services.product_service import (
            ProductService,
        )

        container.get(ProductService).get_top_products = AsyncMock(
            return_value=[
                {
                    "product_id": 1,
                    "name": "Chair",
                    "category": "Furniture",
                    "unit_price": "299.99",
                    "total_sold": 50,
                    "avg_rating": "4.5",
                }
            ]
        )
        resp = client.get("/api/oltp/top-products?limit=3")
        assert resp.status_code == 200
        assert resp.json()[0]["name"] == "Chair"

    def test_product_recommendations(self):
        from src.app.routers.relational.product.services.product_service import (
            ProductService,
        )

        container.get(ProductService).get_product_recommendations = AsyncMock(
            return_value=[
                {
                    "product_id": 2,
                    "name": "Desk",
                    "category": "Furniture",
                    "unit_price": "199.99",
                    "times_bought_together": 15,
                }
            ]
        )
        resp = client.get("/api/oltp/recommendations/1?limit=3")
        assert resp.status_code == 200
        assert resp.json()[0]["product_id"] == 2


# ---------------------------------------------------------------------------
# Document (MongoDB) API tests
# ---------------------------------------------------------------------------

class TestDocumentAPI:
    def test_init_mongodb(self):
        from src.app.routers.document.init_db.services.init_db_service import (
            InitDBService,
        )

        container.get(InitDBService).init_database = AsyncMock(
            return_value={"products": 5, "customers": 3, "purchases": 4}
        )
        resp = client.post("/api/nosql/init")
        assert resp.status_code == 200
        data = resp.json()
        assert data["collections_seeded"]["products"] == 5

    def test_customers_document(self):
        from src.app.routers.document.customer.services.customer_service import (
            CustomerService,
        )

        container.get(CustomerService).get_customers_with_embeddings = AsyncMock(
            return_value=[
                {
                    "id": "507f1f77bcf86cd799439011",
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "email": "alice@example.com",
                    "industry": "Technology",
                    "recent_purchases": [],
                    "matched_products": [],
                    "created_at": "2024-01-15T10:30:00",
                }
            ]
        )
        resp = client.get("/api/nosql/customers?limit=5")
        assert resp.status_code == 200
        assert resp.json()[0]["first_name"] == "Alice"

    def test_products_by_category_document(self):
        from src.app.routers.document.product.services.product_service import (
            ProductService,
        )

        container.get(ProductService).get_products_by_category = AsyncMock(
            return_value=[
                {
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Keyboard",
                    "category": "Electronics",
                    "unit_price": 149.99,
                    "description": "Wireless keyboard",
                    "stock_quantity": 120,
                    "created_at": "2024-01-15T10:30:00",
                }
            ]
        )
        resp = client.get("/api/nosql/products/Electronics")
        assert resp.status_code == 200
        assert resp.json()[0]["category"] == "Electronics"

    def test_purchases_by_customer(self):
        from src.app.routers.document.purchase.services.purchase_service import (
            PurchaseService,
        )

        container.get(PurchaseService).get_purchases_by_customer = AsyncMock(
            return_value=[
                {
                    "id": "507f1f77bcf86cd799439011",
                    "customer_id": "507f1f77bcf86cd799439011",
                    "product_id": "507f1f77bcf86cd799439012",
                    "quantity": 1,
                    "total_amount": 299.99,
                    "purchase_date": "2024-01-15T10:30:00",
                    "payment_method": "credit_card",
                }
            ]
        )
        resp = client.get("/api/nosql/purchases/alice@example.com")
        assert resp.status_code == 200
        assert resp.json()[0]["total_amount"] == 299.99


# ---------------------------------------------------------------------------
# Graph (Neo4j) API tests
# ---------------------------------------------------------------------------

class TestGraphAPI:
    def test_init_neo4j(self):
        from src.app.routers.graph.init_db.services.init_db_service import (
            InitDBService,
        )

        container.get(InitDBService).init_database = AsyncMock(
            return_value={"status": "created"}
        )
        resp = client.post("/api/graph/init")
        assert resp.status_code == 200
        assert resp.json()["status"] == "created"

    def test_purchase_history(self):
        from src.app.routers.graph.customer.services.customer_service import (
            CustomerService,
        )

        container.get(CustomerService).get_purchase_history = AsyncMock(
            return_value=[
                {"product_name": "Keyboard", "category": "Electronics"}
            ]
        )
        resp = client.get("/api/graph/customer-history/alice@example.com")
        assert resp.status_code == 200
        assert resp.json()[0]["product_name"] == "Keyboard"

    def test_recommendations_graph(self):
        from src.app.routers.graph.product.services.product_service import (
            ProductService,
        )

        container.get(ProductService).get_also_bought_recommendations = AsyncMock(
            return_value=[{"product_name": "Mouse", "recommendation_score": 5}]
        )
        resp = client.get("/api/graph/recommendations/Keyboard?limit=3")
        assert resp.status_code == 200
        assert resp.json()[0]["product_name"] == "Mouse"

    def test_top_products_graph(self):
        from src.app.routers.graph.product.services.product_service import (
            ProductService,
        )

        container.get(ProductService).get_top_products = AsyncMock(
            return_value=[{"product_name": "Chair", "purchase_count": 42}]
        )
        resp = client.get("/api/graph/top-products?limit=5")
        assert resp.status_code == 200
        assert resp.json()[0]["product_name"] == "Chair"

    def test_category_products(self):
        from src.app.routers.graph.category.services.category_service import (
            CategoryService,
        )

        container.get(CategoryService).get_products_by_category = AsyncMock(
            return_value=[{"product_name": "Monitor", "product_id": 3}]
        )
        resp = client.get("/api/graph/category-products/Electronics")
        assert resp.status_code == 200
        assert resp.json()[0]["product_name"] == "Monitor"


# ---------------------------------------------------------------------------
# Auth test
# ---------------------------------------------------------------------------

class TestAuth:
    def test_unauthorized_access(self):
        app.dependency_overrides.pop(get_current_user, None)
        try:
            resp = client.get("/api/oltp/customers-with-purchases")
            assert resp.status_code == 403
        finally:
            app.dependency_overrides[get_current_user] = lambda: _fake_user()
