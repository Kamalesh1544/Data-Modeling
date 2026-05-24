Backend Base — Multi-Database B2B Data Platform
A production-grade FastAPI backend demonstrating three database paradigms (Relational, Document, Graph) modeling the same B2B e-commerce domain, with Firebase authentication, async task processing, and full Docker orchestration.
What it does:
Showcases how to model customers, products, purchases, and ratings across PostgreSQL (3NF relational), MongoDB (embedded documents), and Neo4j (graph with collaborative filtering). Each database exposes REST APIs under /api/oltp, /api/nosql, and /api/graph respectively, letting you compare query patterns, data modeling trade-offs, and performance characteristics side by side.
Key features:
- Triple-database architecture — PostgreSQL (normalized OLTP with CHECK constraints, composite indexes, FKs), MongoDB (embedded recent purchases + product matching in customer docs), Neo4j (PURCHASED/ALSO_BOUGHT/BELONGS_TO graph with weighted collaborative filtering)
- 15 REST endpoints — Init/seed each database, query customers with purchase history, top products, category filters, product recommendations, and graph-based collaborative filtering
- Firebase JWT auth — Bearer token verification with get_current_user dependency on every endpoint
- InjectQ DI — Clean singleton/inject pattern across 11 modules (services, repositories, routers)
- Background tasks — Taskiq + Redis async queue with retry middleware
- Infrastructure — Docker Compose (PostgreSQL 16, MongoDB 7, Neo4j 5, Jupyter), GitHub Actions CI (pre-commit, pytest, 80%+ coverage enforcement), Sentry error tracking, Prometheus metrics
- Testing — 60+ passing tests covering DDL validation, Cypher queries, MongoDB aggregations, API integration tests with mocked auth, and dependency overrides
Tech stack: FastAPI, Python 3.12, PostgreSQL/asyncpg, MongoDB/motor, Neo4j, Tortoise ORM, Firebase Admin SDK, Taskiq, Redis, InjectQ, Docker, GitHub Actions
Quick start: docker compose -f docker/docker-compose.yml up -d or SQLite dev mode with uvicorn src.app.main:app --reload
▣  Build · Big Pickle · 2m 43s
it should be in 350 char
+ Thought: 782ms
Backend Base — Production-grade FastAPI backend demonstrating PostgreSQL (3NF), MongoDB (document), and Neo4j (graph) for the same B2B e-commerce domain. Features Firebase auth, async task processing via Taskiq/Redis, Docker Compose orchestration, and 15 REST endpoints with InjectQ dependency injection.
▣  Build · Big Pickle · 4.6s
now givem e a read me file which proper desiging images that show like interst int he user and then give me a proer description and then hw to seup in details with images and animations for gitbug readme fiel that can be anythign like any char ont limit on that prper descrin and then with design images and animation s
+ Thought: 1.2s
→ Read README.md 
+ Thought: 1.5s
# Wrote README.md
<div align="center">
# 🏗️ Multi-Database Data Platform
### Three Databases. One Domain. Production-Grade FastAPI.
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248?logo=mongodb&logoColor=white)](https://mongodb.com)
[![Neo4j](https://img.shields.io/badge/Neo4j-5-4581C3?logo=neo4j&logoColor=white)](https://neo4j.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com)
[![Redis](https://img.shields.io/badge/Redis-Async-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Tests](https://img.shields.io/badge/Tests-60%2B%20%E2%9C%85-success)](https://github.com)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com)
<br>
> **A real-world backend that models the same B2B e-commerce domain across PostgreSQL (Relational/3NF), MongoDB (Document), and Neo4j (Graph) — letting you compare query patterns, data modeling trade-offs, and performance characteristics side by side.**
<br>
</div>
---
## 👀 Why This Project?
```
You're building a data-intensive application and need to choose the right database.
But every database claims to be "the best" — how do you compare them?
This project answers that question by modeling the SAME business domain
in THREE different database paradigms, so you can:
┌────────────────────────────────────────────────────────────────┐
│  🔍  See how the same query (e.g. "top products") is written   │
│      in SQL, MongoDB aggregation, and Neo4j Cypher              │
├────────────────────────────────────────────────────────────────┤
│  ⚖️  Compare data modeling approaches (3NF vs. embedded docs   │
│      vs. graph relationships) for the same entities             │
├────────────────────────────────────────────────────────────────┤
│  🚀  Evaluate real API response formats side-by-side            │
│      — all served from one FastAPI application                  │
├────────────────────────────────────────────────────────────────┤
│  🔐  Production-ready patterns: Firebase auth, DI, background   │
│      tasks, error handling, metrics, Docker deployment          │
└────────────────────────────────────────────────────────────────┘
```
---
## 🏛️ Architecture Overview
<div align="center">
```
                              ┌──────────────────────────────┐
                              │       Firebase Auth          │
                              │   JWT Bearer Token Verify    │
                              └──────────────┬───────────────┘
                                             │
                              ┌──────────────▼───────────────┐
                              │      FastAPI Application      │
                              │    (uvicorn, ORJSON, DI)      │
                              │                               │
                              │  ┌─────────────────────────┐  │
                              │  │   InjectQ DI Container   │  │
                              │  │  Services → Repos → DBs  │  │
                              │  └─────────────────────────┘  │
                              └──┬──────────┬──────────┬──────┘
                                 │          │          │
         ┌───────────────────────┼──────────┼──────────┼───────────────────┐
         │                       │          │          │                    │
         ▼                       ▼          ▼          ▼                    │
  ┌─────────────┐      ┌──────────────┐ ┌──────────┐ ┌──────────────┐      │
  │  Background │      │  PostgreSQL  │ │ MongoDB  │ │    Neo4j     │      │
  │    Tasks    │      │   (3NF SQL)  │ │(Document) │ │   (Graph)    │      │
  │  Taskiq +   │      │              │ │          │ │              │      │
  │   Redis     │      │  /api/oltp   │ │/api/nosql│ │  /api/graph  │      │
  └─────────────┘      └──────────────┘ └──────────┘ └──────────────┘      │
                                                                           │
  ┌────────────────────────────────────────────────────────────────────┐   │
  │  Core Infrastructure                                              │   │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │   │
  │  │  Sentry  │  │  Redis   │  │ Prometheus│  │  Snowflake IDs    │  │   │
  │  │  Errors  │  │  Cache   │  │  Metrics  │  │  Distributed UIDs │  │   │
  │  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘  │   │
  └────────────────────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────────────────┘
```
</div>
---
## 🗄️ Three Databases, One Domain
Each database stores the same entities — `Customer`, `Product`, `Purchase` — but models them very differently.
### 🐘 PostgreSQL — Relational (3NF)
[![DDL](https://img.shields.io/badge/Schema-DDL-blue)](src/app/db/relational/ddl.sql)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PostgreSQL (3NF)                                │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   customers   │    │   products    │    │ user_ratings │               │
│  ├──────────────┤    ├──────────────┤    ├──────────────┤               │
│  │ PK customer_id│    │ PK product_id│    │ PK rating_id │               │
│  │ email (UQ)    │    │ name         │    │ FK customer_id│──────────┐  │
│  │ industry      │    │ category     │    │ FK product_id│─────┐    │  │
│  │ created_at    │    │ unit_price   │    │ rating 1-5   │    │    │  │
│  └──────┬───────┘    │ stock_quantity│    └──────────────┘    │    │  │
│         │            └──────┬───────┘                       │    │  │
│         │                   │                               │    │  │
│         │    ┌──────────────▼──────────────────────────────┐ │    │  │
│         └───►│               purchases                     │◄┘    │  │
│              ├─────────────────────────────────────────────┤      │  │
│              │ PK purchase_id                              │      │  │
│              │ FK customer_id (NOT NULL)────────────────────┘      │  │
│              │ FK product_id  (NOT NULL)───────────────────────────┘  │
│              │ quantity, total_amount, purchase_date                 │
│              │ CHECK constraints on price, quantity, amount          │
│              │ Composite indexes for analytical queries              │
│              └─────────────────────────────────────────────────────┘  │
│  🔗 /api/oltp/customers-with-purchases — JOIN across 3 tables        │
│  🔗 /api/oltp/top-products — GROUP BY + AVG(rating) + ORDER BY       │
│  🔗 /api/oltp/recommendations/{id} — Self-join via purchases         │
└─────────────────────────────────────────────────────────────────────────┘
```
**APIs:**
| Endpoint | Description |
|---|---|
| `POST /api/oltp/init` | Create tables & seed data |
| `GET /api/oltp/customers-with-purchases` | Customers with purchase history |
| `GET /api/oltp/top-products` | Top selling products with avg rating |
| `GET /api/oltp/recommendations/{product_id}` | Product recommendations (also-bought) |
### 🍃 MongoDB — Document
[![Aggregation](https://img.shields.io/badge/Query-Aggregation%20Pipeline-green)](src/app/db/nosql)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          MongoDB (Document)                              │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  customers collection                                            │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │  {                                                               │   │
│  │    _id: ObjectId,                                                │   │
│  │    first_name: "Alice", last_name: "Johnson",                    │   │
│  │    email: "alice@example.com",  industry: "Technology",          │   │
│  │    recent_purchases: [  ← EMBEDDED (10 most recent)             │   │
│  │      { product_id, product_name, amount, date }, ...             │   │
│  │    ],                                                            │   │
│  │    matched_products: [  ← EMBEDDED (industry-matched)           │   │
│  │      { product_id, product_name, reason }, ...                   │   │
│  │    ]                                                             │   │
│  │  }                                                               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  products collection                                            │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │  { _id: ObjectId, name: "Mechanical Keyboard",                  │   │
│  │    category: "Electronics", unit_price: 149.99,                 │   │
│  │    switch_type: "Cherry MX Blue"  ← VARYING FIELDS per category │   │
│  │  }                                                               │   │
│  │  { _id: ObjectId, name: "4K Monitor", category: "Electronics",  │   │
│  │    unit_price: 499.99, resolution: "3840x2160",                 │   │
│  │    ports: ["HDMI", "DisplayPort"]  ← category-specific fields   │   │
│  │  }                                                               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  purchases collection  ← REFERENCING (unbounded growth)         │   │
│  │  { _id, customer_id, product_id, quantity, total_amount, ... }  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```
**APIs:**
| Endpoint | Description |
|---|---|
| `POST /api/nosql/init` | Initialize collections & seed |
| `GET /api/nosql/customers` | Customers with embedded documents |
| `GET /api/nosql/products/{category}` | Products filtered by category |
| `GET /api/nosql/purchases/{email}` | Purchases by customer email |
### 🔮 Neo4j — Graph
[![Cypher](https://img.shields.io/badge/Query-Cypher-4581C3)](src/app/db/graph/cypher_queries.cypher)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Neo4j (Graph)                                   │
│                                                                          │
│                    ┌──────────────┐                                      │
│                    │   Customer    │ ◄── Person node                     │
│                    │  (alice@...) │                                      │
│                    └──────┬───────┘                                      │
│                           │                                              │
│                           │ PURCHASED {quantity: 2, amount: 299.98}     │
│                           ▼                                              │
│     ┌─────────────────────────────────────────────────────────┐         │
│     │                      Product                             │         │
│     │                  ("Mechanical Keyboard")                 │         │
│     └──┬──────────────┬──────────────────────┬────────────────┘         │
│        │              │                      │                           │
│        │ ALSO_BOUGHT  │ ALSO_BOUGHT          │ BELONGS_TO                │
│        │ strength:0.8 │ strength:0.6         │                           │
│        ▼              ▼                      ▼                           │
│  ┌──────────┐  ┌──────────────┐   ┌────────────────┐                    │
│  │ Product  │  │   Product    │   │   Category      │                    │
│  │ ("Mouse")│  │ ("Monitor")  │   │ ("Electronics") │                    │
│  └──────────┘  └──────────────┘   └────────────────┘                    │
│                                                                          │
│  🔗 Collaborative filtering: Customer → PURCHASED → Product ← ALSO_BOUGHT → Recommendation │
│  🔗 Category traversal: Category ← BELONGS_TO ← Product              │
│  🔗 Top products: Count PURCHASED relationships per product           │
└─────────────────────────────────────────────────────────────────────────┘
```
**APIs:**
| Endpoint | Description |
|---|---|
| `POST /api/graph/init` | Create graph schema & seed |
| `GET /api/graph/recommendations/{name}` | Also-bought recommendations |
| `GET /api/graph/customer-history/{email}` | Customer purchase history |
| `GET /api/graph/category-products/{category}` | Products in a category |
| `GET /api/graph/top-products` | Top products by purchase count |
---
## ⚡ Quick Start
### 🐳 Full Stack with Docker (Recommended)
```bash
# 1. Clone and enter the project
git clone https://github.com/your-org/backend-base.git
cd backend-base
# 2. Configure environment
cp .env.example .env
# 3. Launch everything
docker compose -f docker/docker-compose.yml up -d
```
That's it! After the containers are healthy:
| Service | URL | Credentials |
|---|---|---|
| **FastAPI App** | `http://localhost:8082` | — |
| **Swagger Docs** | `http://localhost:8082/docs` | — |
| **ReDoc** | `http://localhost:8082/redocs` | — |
| **Neo4j Browser** | `http://localhost:7474` | `neo4j / password` |
| **Jupyter Lab** | `http://localhost:8888` | token from logs |
| **PostgreSQL** | `localhost:5432` | `postgres / postgres` |
| **MongoDB** | `localhost:27017` | — |
```bash
# 4. Initialize databases (pick one)
#    Option A: Via API
curl -X POST http://localhost:8082/api/oltp/init
curl -X POST http://localhost:8082/api/nosql/init
curl -X POST http://localhost:8082/api/graph/init
#    Option B: Via CLI script
python scripts/init_databases.py
```
### 💻 Local Development (SQLite)
No Docker required — runs with SQLite for auth tables plus mock data:
```bash
# Create virtual environment
python -m venv .venv && source .venv/bin/activate  # Linux/Mac
python -m venv .venv && .venv\Scripts\activate     # Windows
# Install dependencies
pip install -r docker/requirements.txt
# Set environment
set DATABASE_TYPE=sqlite  # Windows
export DATABASE_TYPE=sqlite  # Linux/Mac
# Run the app
uvicorn src.app.main:app --reload --host localhost --port 8082
```
---
## 🧪 Testing & Quality
<div align="center">
<table>
<tr>
<td align="center"><b>Category</b></td>
<td align="center"><b>Command</b></td>
<td align="center"><b>What it checks</b></td>
</tr>
<tr>
<td><b>All Tests</b></td>
<td><code>pytest</code></td>
<td>60+ tests across all modules</td>
</tr>
<tr>
<td><b>API Tests</b></td>
<td><code>pytest src/tests/data_platform_tests/test_api.py -v</code></td>
<td>14 integration tests with mocked auth</td>
</tr>
<tr>
<td><b>DDL Tests</b></td>
<td><code>pytest src/tests/data_platform_tests/test_postgres_ddl.py -v</code></td>
<td>DDL syntax, constraints, indexes, types</td>
</tr>
<tr>
<td><b>MongoDB Tests</b></td>
<td><code>pytest src/tests/data_platform_tests/test_mongodb.py -v</code></td>
<td>Aggregation pipelines, embedding logic</td>
</tr>
<tr>
<td><b>Neo4j Tests</b></td>
<td><code>pytest src/tests/data_platform_tests/test_neo4j.py -v</code></td>
<td>Cypher queries, graph traversal patterns</td>
</tr>
<tr>
<td><b>Coverage</b></td>
<td><code>pytest --cov=src --cov-report=term-missing</code></td>
<td>80%+ coverage enforced in CI</td>
</tr>
<tr>
<td><b>Linting</b></td>
<td><code>ruff check src/</code></td>
<td>Ruff (line-length 100, Python 3.12)</td>
</tr>
<tr>
<td><b>Type Check</b></td>
<td><code>mypy src/</code></td>
<td>Static type checking</td>
</tr>
<tr>
<td><b>Security</b></td>
<td><code>bandit -r src/</code></td>
<td>Security vulnerability scan</td>
</tr>
</table>
</div>
---
## 📁 Project Structure
```
backend-base/
├── src/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point
│   │   ├── worker.py                   # Taskiq background worker
│   │   ├── core/
│   │   │   ├── auth/                   # Firebase JWT authentication
│   │   │   ├── config/                 # Settings, logging, middleware, Sentry
│   │   │   ├── exceptions/             # Global error handlers
│   │   │   ├── di.py                   # InjectQ container setup
│   │   │   └── snowflake.py            # Snowflake ID generator
│   │   ├── db/
│   │   │   ├── relational/ddl.sql      # PostgreSQL DDL (3NF schema)
│   │   │   ├── nosql/                  # MongoDB aggregation pipelines
│   │   │   ├── graph/cypher_queries.cypher  # Neo4j Cypher scripts
│   │   │   ├── seed_data/              # CSV seed data (customers, products, etc.)
│   │   │   ├── tables/                 # Tortoise ORM models (auth)
│   │   │   └── setup_database.py       # Multi-DB initialization
│   │   ├── routers/
│   │   │   ├── auth/                   # User management endpoints
│   │   │   ├── relational/             # PostgreSQL endpoints (3 modules)
│   │   │   ├── document/               # MongoDB endpoints (4 modules)
│   │   │   └── graph/                  # Neo4j endpoints (4 modules)
│   │   ├── tasks/                      # Background task definitions
│   │   └── utils/                      # Response helpers, schemas
│   └── tests/
│       ├── data_platform_tests/        # 45+ tests for data layer
│       ├── integration_tests/          # Auth API integration tests
│       ├── task_tests/                 # Background task tests
│       └── unit_tests/                 # Unit tests (config, snowflake)
├── docker/
│   ├── Dockerfile                      # Python 3.12 container
│   ├── docker-compose.yml              # Full stack orchestration
│   └── requirements.txt                # Python dependencies
├── scripts/
│   ├── init_databases.py               # Seed all 3 databases
│   └── generate_docs.py                # Auto-doc generation
├── notebooks/
│   └── data_platform_exploration.ipynb # Interactive exploration
├── .github/workflows/
│   ├── formatting_and_pytest.yml       # CI: lint + test on PR
│   └── coverage_report.yml             # CI: coverage enforcement
└── .pre-commit-config.yaml             # Pre-commit hooks
```
---
## 🛠️ Tech Stack
<div align="center">
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688) | Async Python web framework |
| **Server** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.30-2334) | ASGI server |
| **Relational** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1) + **asyncpg** | 3NF OLTP schema |
| **OR/M** | ![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-0.25-green) | Auth table models + migrations (Aerich) |
| **Document** | ![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248) + **motor** | Embedded document store |
| **Graph** | ![Neo4j](https://img.shields.io/badge/Neo4j-5-4581C3) + **neo4j** | Graph traversal & recommendations |
| **Auth** | ![Firebase](https://img.shields.io/badge/Firebase%20Admin-6.5-FFCA28) | JWT token verification |
| **DI** | ![InjectQ](https://img.shields.io/badge/InjectQ-0.3-blueviolet) | Singleton + inject decorators |
| **Tasks** | ![Taskiq](https://img.shields.io/badge/Taskiq-0.11-blue) + **Redis** | Async background task queue |
| **IDs** | ![SnowflakeKit](https://img.shields.io/badge/SnowflakeKit-0.1-lightblue) | Distributed unique ID generation |
| **Errors** | ![Sentry](https://img.shields.io/badge/Sentry-2.10-362D59) | Error tracking & monitoring |
| **Metrics** | ![Prometheus](https://img.shields.io/badge/Prometheus--Instrumentator-7.1-E6522C) | API instrumentation |
| **Containers** | ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED) | Full-stack orchestration |
| **CI/CD** | ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF) | Lint, test, coverage enforcement |
| **Quality** | ![Ruff](https://img.shields.io/badge/Ruff-Linter-D7FF64) + **Mypy** + **Bandit** | Lint, types, security |
</div>
---
## ✨ Key Design Decisions
| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **3NF normalization** in PostgreSQL | Eliminates data redundancy; CHECK constraints enforce domain integrity (price ≥ 0, rating 1-5) |
| 2 | **Embedded recent purchases** in MongoDB customers | Optimizes the "customer profile" read — one query returns customer + last 10 purchases |
| 3 | **Flexible product schema** in MongoDB | Each product category has different attributes (monitors have resolution/ports; keyboards have switch type) |
| 4 | **Referenced purchases** in MongoDB | Purchases grow unboundedly — embedding them would exceed document size limits |
| 5 | **Weighted ALSO_BOUGHT** relationships in Neo4j | `strength (0.0-1.0)` enables ranked collaborative filtering via graph traversal |
| 6 | **BELONGS_TO** category grouping in Neo4j | Enables category-based product traversal without full-text search |
| 7 | **Per-endpoint JWT auth** | Every data platform endpoint explicitly declares `Depends(get_current_user)` — no surprise auth |
| 8 | **InjectQ singleton pattern** | Services and repositories are singletons resolved at runtime — clean DI without framework coupling |
| 9 | **Tortoise ORM for auth only** | User management uses a proper async ORM with migrations; data platform uses raw drivers for full control |
| 10 | **Seed data in test files** | Repos accept data as parameters — no hardcoded test data in production code |
---
## 🔐 Authentication
All data platform endpoints require a Firebase JWT Bearer token:
```http
Authorization: Bearer <firebase-id-token>
```
- **Flow:** Extract token → `auth.verify_id_token(token)` → decode into `AuthUserSchema`
- **On failure:** Returns `403` with error codes: `REVOKED_TOKEN`, `USER_ACCOUNT_DISABLE`, `INVALID_TOKEN`
- **Testing:** Override via `app.dependency_overrides[get_current_user]` — tests inject a fake admin user
---
## 🧰 Background Tasks
Taskiq + Redis handles async processing:
```python
# Define a task
@task
async def user_service_post_processing(user_id: UUID):
    await some_heavy_computation(user_id)
# Run the worker
taskiq worker src.app.worker:broker -fsd -tp 'src/**/*_tasks.py' --reload
```
Features: `SimpleRetryMiddleware` (3 retries), `MonitoringMiddleware` (logging), InMemoryBroker fallback for tests.
---
## 📊 Database Comparison (Same Queries)
| Query | PostgreSQL (SQL) | MongoDB (Aggregation) | Neo4j (Cypher) |
|-------|-----------------|----------------------|----------------|
| Top Products | `GROUP BY product_id ORDER BY COUNT(*) DESC` | `$group by product_id → $sort by count` | `MATCH (:Customer)-[:PURCHASED]->(p:Product) RETURN p ORDER BY count(p) DESC` |
| Customer History | `JOIN purchases ON customers.id = purchases.customer_id` | `$match email → $lookup purchases` | `MATCH (c:Customer {email})-[:PURCHASED]->(p:Product) RETURN p` |
| Product Recommendations | Self-join on purchases for co-occurrence | Custom aggregation pipeline | `MATCH (p:Product)<-[:PURCHASED]-()-[:PURCHASED]->(rec)` |
| Category Filter | `WHERE category = 'Electronics'` | `$match { category: 'Electronics' }` | `MATCH (cat:Category {name})-[:BELONGS_TO]-(p:Product)` |
---
## 📈 CI/CD Pipeline
<div align="center">
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  PR to   │───►│  Pre-    │───►│  Pytest  │───►│  Codecov │───►│  Merge   │
│   dev    │    │  commit  │    │  80%+    │    │  Report  │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │               │
                     ▼               ▼
                 ruff lint      coverage.xml
                 mypy types     + HTML report
                 bandit sec
```
</div>
---
## 🚢 Docker Compose Services
```yaml
services:
  postgres:   # PostgreSQL 16 Alpine on :5432
  mongodb:    # MongoDB 7 on :27017
  neo4j:      # Neo4j 5 Community on :7474 (HTTP) + :7687 (Bolt)
  base_app:   # FastAPI app on :8082 (depends on all DBs with health checks)
  jupyter:    # Jupyter notebook server on :8888
```
All services connected via `data_network` bridge with named volumes for persistence.
---
## 📝 License
MIT
---
<div align="center">
### Built with ❤️ for the data-curious developer
**[Swagger Docs](http://localhost:8082/docs)** • **[ReDoc](http://localhost:8082/redocs)** • **[Neo4j Browser](http://localhost:7474)**
</div>
