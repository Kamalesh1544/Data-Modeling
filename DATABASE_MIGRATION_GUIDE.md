# Database Migration Guide

## Overview
This project supports both SQLite (for development) and PostgreSQL (for production). This guide explains how to switch between them.

## Current Setup: SQLite (Development)

### Prerequisites
- Python environment with all dependencies installed from `requirements.txt`
- The `aiosqlite` package is already included in requirements

### Configuration
Your `.env` file should have:
```env
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=./db.sqlite3
```

### Initialize Database
```bash
# Initialize Aerich (only needed once)
aerich init -t src.app.db.setup_database.TORTOISE_ORM

# Create initial database schema
aerich init-db

# The database file will be created at ./db.sqlite3
```

### Running Migrations
```bash
# Generate migration files after model changes
aerich migrate --name "your_migration_name"

# Apply migrations
aerich upgrade

# Revert migrations (if needed)
aerich downgrade
```

## Switching to PostgreSQL (Production)

### Prerequisites
1. Install and run PostgreSQL server
2. Create a database and user with appropriate permissions

### Step 1: Update Environment Variables
Update your `.env` file:
```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=your-postgres-host
POSTGRES_PORT=5432
POSTGRES_USER=your-postgres-user
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_DB=your-database-name
POSTGRES_SCHEMA=cv
```

### Step 2: Backup SQLite Data (Optional)
If you have data in SQLite that you want to migrate:
```bash
# Export data from SQLite
# You'll need to write custom scripts or use tools like pgloader
```

### Step 3: Initialize PostgreSQL Database
```bash
# The migrations should already exist, just apply them
aerich upgrade

# If starting fresh, you can:
# aerich init-db
```

### Step 4: Restart Application
```bash
# Stop the application
# The application will now connect to PostgreSQL

# Start the application
uvicorn src.app.main:app --reload
```

## Switching Back to SQLite

Simply update your `.env` file back to SQLite configuration and restart the application:
```env
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=./db.sqlite3
```

## Docker Setup

### Using Docker with SQLite
The docker-compose.yml is configured to mount the SQLite database file:
```bash
docker-compose up
```

### Using Docker with PostgreSQL
1. Update `.env` file with PostgreSQL settings
2. Ensure PostgreSQL is accessible from Docker network
3. Run docker-compose:
```bash
docker-compose up
```

## Database URL Format Reference

### SQLite
```python
"sqlite://path/to/database.db"  # Relative path
"sqlite:///absolute/path/to/database.db"  # Absolute path
"sqlite://:memory:"  # In-memory database (for testing)
```

### PostgreSQL
```python
"postgres://user:password@host:port/database"
```

## Troubleshooting

### Issue: "No such table" error
**Solution:** Run migrations:
```bash
aerich upgrade
```

### Issue: PostgreSQL connection refused
**Solution:** 
- Check if PostgreSQL is running
- Verify host and port in `.env`
- Check firewall settings
- Verify user permissions

### Issue: SQLite database locked
**Solution:**
- Close all connections to the database
- Restart the application
- Check if another process is using the database

### Issue: Migration conflicts
**Solution:**
```bash
# Check migration history
aerich history

# If needed, downgrade and reapply
aerich downgrade
aerich upgrade
```

## Best Practices

1. **Development**: Use SQLite for quick local development and testing
2. **Staging/Production**: Use PostgreSQL for production workloads
3. **Version Control**: Commit migration files but not database files
4. **Backups**: Always backup your database before running migrations
5. **Testing**: Test migrations on a copy of production data before deploying

## Performance Considerations

### SQLite
- ✅ Perfect for development and testing
- ✅ No setup required
- ✅ Single file, easy to backup
- ❌ Limited concurrent write operations
- ❌ Not suitable for high-traffic production

### PostgreSQL
- ✅ Excellent for production
- ✅ Handles concurrent connections well
- ✅ Advanced features (schemas, full-text search, etc.)
- ✅ Better performance for large datasets
- ❌ Requires separate server setup

## Environment-Specific Configuration

### Local Development
```env
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=./db.sqlite3
```

### Docker Development
```env
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=./db.sqlite3
```

### Staging
```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=staging-db.example.com
POSTGRES_PORT=5432
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_password
POSTGRES_DB=staging_db
POSTGRES_SCHEMA=cv
```

### Production
```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=prod-db.example.com
POSTGRES_PORT=5432
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=strong_password
POSTGRES_DB=prod_db
POSTGRES_SCHEMA=cv
```
