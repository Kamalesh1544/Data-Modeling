#!/usr/bin/env python3
"""
Validation script to check database configuration.
Run this after installing dependencies to verify the setup.
"""

import sys


try:
    from src.app.core.config.settings import get_settings
    from src.app.db.setup_database import TORTOISE_ORM, get_database_config

    print("=" * 60)
    print("Database Configuration Validation")
    print("=" * 60)

    settings = get_settings()
    print("\n✓ Settings loaded successfully")
    print(f"  Database Type: {settings.DATABASE_TYPE}")

    if settings.DATABASE_TYPE.lower() == "sqlite":
        print(f"  SQLite Path: {settings.SQLITE_DB_PATH}")
    elif settings.DATABASE_TYPE.lower() == "postgresql":
        print(f"  PostgreSQL Host: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")
        print(f"  Database: {settings.POSTGRES_DB}")
        print(f"  Schema: {settings.POSTGRES_SCHEMA}")

    print("\n✓ Getting database configuration...")
    config = get_database_config()
    print(f"  Engine: {config['engine']}")

    print("\n✓ TORTOISE_ORM configuration:")
    print(f"  Connections: {list(TORTOISE_ORM['connections'].keys())}")
    print(f"  Apps: {list(TORTOISE_ORM['apps'].keys())}")

    print("\n" + "=" * 60)
    print("✅ All configuration checks passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: aerich init -t src.app.db.setup_database.TORTOISE_ORM")
    print("2. Run: aerich init-db")
    print("3. Run: uvicorn src.app.main:app --reload")

except Exception as e:
    print("\n" + "=" * 60)
    print("❌ Configuration validation failed!")
    print("=" * 60)
    print(f"\nError: {e}")
    print("\nMake sure you have:")
    print("1. Installed all dependencies: pip install -r requirements.txt")
    print("2. Created a .env file: cp .env.example .env")
    sys.exit(1)
