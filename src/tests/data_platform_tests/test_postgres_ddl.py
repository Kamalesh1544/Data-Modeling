"""Tests for PostgreSQL DDL schema (3NF compliance)."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest


DDL_PATH = Path(__file__).resolve().parent.parent.parent / "app" / "db" / "relational" / "ddl.sql"


@pytest.fixture
def ddl_content() -> str:
    return DDL_PATH.read_text(encoding="utf-8")


class TestPostgresDDL:
    def test_ddl_file_exists(self) -> None:
        assert DDL_PATH.exists(), f"DDL file not found at {DDL_PATH}"

    def test_ddl_creates_customers_table(self, ddl_content: str) -> None:
        assert "CREATE TABLE customers" in ddl_content

    def test_ddl_creates_products_table(self, ddl_content: str) -> None:
        assert "CREATE TABLE products" in ddl_content

    def test_ddl_creates_purchases_table(self, ddl_content: str) -> None:
        assert "CREATE TABLE purchases" in ddl_content

    def test_ddl_creates_user_ratings_table(self, ddl_content: str) -> None:
        assert "CREATE TABLE user_ratings" in ddl_content

    def test_no_repeating_groups(self, ddl_content: str) -> None:
        lines_no_comments = "\n".join(
            line for line in ddl_content.splitlines()
            if not line.strip().startswith("--")
        )
        assert "JSON" not in lines_no_comments.upper()
        assert "ARRAY" not in lines_no_comments.upper()

    def test_primary_keys_defined(self, ddl_content: str) -> None:
        assert "PRIMARY KEY" in ddl_content

    def test_foreign_keys_defined(self, ddl_content: str) -> None:
        assert "REFERENCES" in ddl_content

    def test_numeric_types_used(self, ddl_content: str) -> None:
        assert "NUMERIC" in ddl_content
        assert "INTEGER" in ddl_content
        assert "SMALLINT" in ddl_content

    def test_timestamp_types_used(self, ddl_content: str) -> None:
        assert "TIMESTAMPTZ" in ddl_content

    def test_varchar_not_only_type(self, ddl_content: str) -> None:
        assert "TEXT" in ddl_content

    def test_check_constraints_defined(self, ddl_content: str) -> None:
        assert "CHECK" in ddl_content

    def test_indexes_defined(self, ddl_content: str) -> None:
        assert "CREATE INDEX" in ddl_content


class TestCSVSeedData:
    @pytest.fixture
    def seed_dir(self) -> Path:
        return DDL_PATH.parent.parent / "seed_data"

    def test_customers_csv_exists(self, seed_dir: Path) -> None:
        assert (seed_dir / "customers.csv").exists()

    def test_products_csv_exists(self, seed_dir: Path) -> None:
        assert (seed_dir / "products.csv").exists()

    def test_purchases_csv_exists(self, seed_dir: Path) -> None:
        assert (seed_dir / "purchases.csv").exists()

    def test_user_ratings_csv_exists(self, seed_dir: Path) -> None:
        assert (seed_dir / "user_ratings.csv").exists()

    def test_products_csv_has_numeric_price(self, seed_dir: Path) -> None:
        with (seed_dir / "products.csv").open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                price = float(row["unit_price"])
                assert price >= 0, f"Negative price found: {price}"

    def test_purchases_csv_has_valid_amounts(self, seed_dir: Path) -> None:
        with (seed_dir / "purchases.csv").open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total = float(row["total_amount"])
                assert total >= 0, f"Negative total_amount: {total}"
