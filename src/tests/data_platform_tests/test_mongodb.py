"""Tests for MongoDB document model (embedding, referencing, flexible schemas)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from src.app.routers.document.customer.repositories.customer_repo import (
    CustomerRepo,
)
from src.app.routers.document.init_db.repositories.init_db_repo import (
    InitDBRepo,
)
from src.app.routers.document.product.repositories.product_repo import (
    ProductRepo,
)


EXPECTED_PRODUCT_COUNT = 5
EXPECTED_CUSTOMER_COUNT = 3
EXPECTED_PURCHASE_COUNT = 4
MIN_PRODUCT_VARIATIONS = 3
VALID_OID = "507f1f77bcf86cd799439011"

PRODUCT_SEED_DATA: list[dict[str, Any]] = [
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


def build_customer_seed_data(pids: list[ObjectId]) -> list[dict[str, Any]]:
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


def build_purchase_seed_data(cids: list[ObjectId], pids: list[ObjectId]) -> list[dict[str, Any]]:
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


@pytest.fixture
def valid_ids() -> list[str]:
    return [f"{i:024x}" for i in range(1, 6)]


@pytest.fixture
def customer_repo() -> CustomerRepo:
    return CustomerRepo()


@pytest.fixture
def product_repo() -> ProductRepo:
    return ProductRepo()


@pytest.fixture
def init_repo() -> InitDBRepo:
    return InitDBRepo()


class TestMongoDBSetup:
    def test_get_client_default_uri(self) -> None:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        assert client is not None

    def test_get_db_default_name(self) -> None:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["ecommerce_nosql"]
        assert db.name == "ecommerce_nosql"

    def test_get_db_custom_name(self) -> None:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["test_db"]
        assert db.name == "test_db"

    @pytest.mark.asyncio
    async def test_seed_products_creates_documents_with_varying_fields(
        self, product_repo: ProductRepo
    ) -> None:
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_collection.insert_many = AsyncMock(
            return_value=MagicMock(inserted_ids=[VALID_OID] * 5)
        )

        ids = await product_repo.seed_products(mock_db, PRODUCT_SEED_DATA)
        assert len(ids) == EXPECTED_PRODUCT_COUNT

        call_args = mock_collection.insert_many.call_args
        documents: list[dict[str, Any]] = call_args[0][0]
        assert len(documents) >= MIN_PRODUCT_VARIATIONS

        keyboard = next(d for d in documents if "Wireless" in d["name"])
        assert "switch_type" in keyboard
        assert "battery_life_hours" in keyboard

        monitor = next(d for d in documents if "Monitor" in d["name"])
        assert "resolution" in monitor
        assert "ports" in monitor

        chair = next(d for d in documents if "Chair" in d["name"])
        assert "material" in chair
        assert "warranty_years" in chair

    @pytest.mark.asyncio
    async def test_init_collections_creates_required_collections(
        self, init_repo: InitDBRepo
    ) -> None:
        mock_db = AsyncMock()
        mock_db.list_collection_names = AsyncMock(return_value=[])
        mock_db.create_collection = AsyncMock()

        await init_repo.init_collections(mock_db)

        expected = {"customers", "products", "purchases"}
        created = {call[0][0] for call in mock_db.create_collection.call_args_list}
        assert created == expected, f"Missing collections: {expected - created}"

    def test_serialize_doc_converts_objectid(self) -> None:
        repo = CustomerRepo()
        doc = {"_id": ObjectId(VALID_OID), "name": "test"}
        result = repo._serialize_doc(doc)  # type: ignore[no-untyped-call]
        assert "id" in result
        assert result["id"] == VALID_OID
        assert "_id" not in result
        assert result["name"] == "test"


class TestMongoDBQueries:
    @pytest.mark.asyncio
    async def test_get_customers_with_embeddings(
        self, customer_repo: CustomerRepo
    ) -> None:
        mock_db = MagicMock()
        mock_coll = MagicMock()
        mock_db.__getitem__.return_value = mock_coll

        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = [
            {
                "_id": MagicMock(),
                "first_name": "Alice",
                "recent_purchases": [],
                "matched_products": [],
            },
        ]
        mock_coll.find.return_value = MagicMock(limit=MagicMock(return_value=mock_cursor))

        results = await customer_repo.get_customers_with_embeddings(mock_db, 10)
        assert len(results) == 1
        assert results[0]["first_name"] == "Alice"

    @pytest.mark.asyncio
    async def test_get_products_by_category_filters_correctly(
        self, product_repo: ProductRepo
    ) -> None:
        mock_db = MagicMock()
        mock_coll = MagicMock()
        mock_db.__getitem__.return_value = mock_coll

        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = [
            {"_id": MagicMock(), "name": "Keyboard", "category": "Electronics"},
        ]
        mock_coll.find.return_value = mock_cursor

        results = await product_repo.get_products_by_category(mock_db, "Electronics")
        assert len(results) == 1
        mock_coll.find.assert_called_once_with({"category": "Electronics"})

    @pytest.mark.asyncio
    async def test_seed_all_returns_counts(
        self, valid_ids: list[str], init_repo: InitDBRepo
    ) -> None:
        mock_db = AsyncMock()
        mock_coll = MagicMock()
        mock_db.__getitem__.return_value = mock_coll

        counts = await init_repo.seed_all(
            mock_db,
            product_ids=valid_ids,
            customer_ids=valid_ids[:EXPECTED_CUSTOMER_COUNT],
            purchase_ids=valid_ids[:EXPECTED_PURCHASE_COUNT],
        )
        assert counts["products"] == EXPECTED_PRODUCT_COUNT
        assert counts["customers"] == EXPECTED_CUSTOMER_COUNT
        assert counts["purchases"] == EXPECTED_PURCHASE_COUNT

