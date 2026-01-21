# SQLite Setup Checklist

Use this checklist to set up your backend with SQLite database.

## Initial Setup

### ☐ 1. Clone Repository
```bash
git clone https://github.com/10XScale-in/backend-base.git
cd backend-base
```

### ☐ 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### ☐ 3. Install Dependencies
```bash
pip install -r requirements.txt
```
**Verify:** Check that `aiosqlite` is installed
```bash
pip list | grep aiosqlite
```

### ☐ 4. Configure Environment
```bash
cp .env.example .env
```
**Verify:** Check that `.env` contains:
- `DATABASE_TYPE=sqlite`
- `SQLITE_DB_PATH=./db.sqlite3`

### ☐ 5. Validate Configuration (Optional)
```bash
python3 scripts/validate_db_config.py
```
**Expected:** See "✅ All configuration checks passed!"

## Database Initialization

### ☐ 6. Initialize Aerich
```bash
aerich init -t src.app.db.setup_database.TORTOISE_ORM
```
**Verify:** Check that `pyproject.toml` has Aerich configuration

### ☐ 7. Create Database Schema
```bash
aerich init-db
```
**Verify:** Check that `db.sqlite3` file is created in project root

### ☐ 8. Check Database File
```bash
ls -lh db.sqlite3
```
**Expected:** File should exist and be a few KB in size

## Run Application

### ☐ 9. Start FastAPI Server
```bash
uvicorn src.app.main:app --reload --host localhost --port 8082
```
**Expected:** See "Application startup complete"

### ☐ 10. Test API Documentation
Open in browser:
- http://localhost:8082/docs
- http://localhost:8082/redocs

**Verify:** Swagger UI loads successfully

### ☐ 11. Test Health Endpoint
```bash
curl http://localhost:8082/
```
**Expected:** Get a response from the API

## Optional Steps

### ☐ 12. Run Tests
```bash
pytest
```
**Expected:** Tests pass (or check which fail)

### ☐ 13. Run Worker (If using background tasks)
```bash
taskiq worker src.app.worker:broker -fsd -tp 'src/**/*_tasks.py' --reload
```

### ☐ 14. View Database (Optional)
Install DB Browser for SQLite:
- macOS: `brew install --cask db-browser-for-sqlite`
- Windows/Linux: Download from https://sqlitebrowser.org/

Open `db.sqlite3` file to view tables and data.

## Docker Setup (Alternative)

### ☐ 15. Build Docker Image
```bash
docker-compose build
```

### ☐ 16. Start Docker Services
```bash
docker-compose up
```
**Verify:** Services start without errors

### ☐ 17. Check Docker Logs
```bash
docker-compose logs -f base_app
```

## Database Operations

### ☐ 18. Make Model Changes
Edit files in `src/app/db/tables/`

### ☐ 19. Generate Migration
```bash
aerich migrate --name "describe_your_changes"
```

### ☐ 20. Apply Migration
```bash
aerich upgrade
```

### ☐ 21. Verify Migration
```bash
aerich history
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'aiosqlite'"
**Solution:**
```bash
pip install aiosqlite
# Or reinstall all dependencies
pip install -r requirements.txt
```

### Problem: "Database is locked"
**Solution:**
```bash
# Stop all running instances
# Kill process using the database
lsof db.sqlite3
kill -9 <PID>
```

### Problem: "Permission denied: db.sqlite3"
**Solution:**
```bash
chmod 644 db.sqlite3
```

### Problem: "No such table" error
**Solution:**
```bash
# Run migrations
aerich upgrade
# Or reinitialize
rm db.sqlite3
aerich init-db
```

### Problem: Port 8082 already in use
**Solution:**
```bash
# Use different port
uvicorn src.app.main:app --reload --port 8083
```

## Success Criteria

✅ Virtual environment activated
✅ All dependencies installed
✅ `.env` file configured
✅ `db.sqlite3` file created
✅ Migrations applied
✅ API server running
✅ API documentation accessible
✅ Tests passing (optional)

## Next Steps After Setup

1. **Read the documentation**
   - [README.md](README.md) - Full documentation
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md) - Database guide

2. **Develop your features**
   - Add models in `src/app/db/tables/`
   - Add routes in `src/app/routers/`
   - Add tests in `src/tests/`

3. **When ready for production**
   - Follow [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md)
   - Switch to PostgreSQL
   - Deploy your application

## Quick Reference Commands

```bash
# Start development server
uvicorn src.app.main:app --reload

# Run tests
pytest

# Generate migration
aerich migrate --name "migration_name"

# Apply migrations
aerich upgrade

# View migration history
aerich history

# Start worker
taskiq worker src.app.worker:broker -fsd -tp 'src/**/*_tasks.py' --reload

# Docker
docker-compose up
docker-compose down
docker-compose logs -f
```

## Support

If you encounter any issues:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md)
3. Check that all prerequisites are met
4. Verify your `.env` configuration

---

**Happy coding! 🚀**
