# 🏗️ Multi-Database Data Platform

<div align="center">

# 🚀 Three Databases. One Domain. Production-Grade FastAPI Backend.

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="70"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="70"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original.svg" width="70"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" width="70"/>

<br><br>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-7-47A248?logo=mongodb&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-5-4581C3?logo=neo4j&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?logo=firebase&logoColor=black)
![Redis](https://img.shields.io/badge/Redis-Async-DC382D?logo=redis&logoColor=white)

---

### ⚡ A production-grade FastAPI backend demonstrating:
### PostgreSQL (3NF) + MongoDB (Document) + Neo4j (Graph)

</div>

---

# 📖 About The Project

This project showcases how the **same B2B e-commerce domain** can be modeled across:

- 🐘 PostgreSQL (Relational Database)
- 🍃 MongoDB (Document Database)
- 🔮 Neo4j (Graph Database)

The goal is to compare:

✅ Query patterns  
✅ Data modeling approaches  
✅ Performance characteristics  
✅ Relationship handling  
✅ Recommendation systems  

All databases are exposed through separate REST APIs:

| Database | API Route |
|---|---|
| PostgreSQL | `/api/oltp` |
| MongoDB | `/api/nosql` |
| Neo4j | `/api/graph` |

---

# ✨ Key Features

## 🐘 PostgreSQL Features

- 3NF Normalized Schema
- Foreign Keys
- Composite Indexes
- CHECK Constraints
- JOIN Queries
- Aggregation Queries

---

## 🍃 MongoDB Features

- Embedded Documents
- Aggregation Pipelines
- Flexible Product Schema
- Customer Purchase Embedding
- Dynamic Category Fields

---

## 🔮 Neo4j Features

- Graph Traversal
- PURCHASED Relationships
- ALSO_BOUGHT Relationships
- Collaborative Filtering
- Recommendation Engine

---

## ⚙️ Infrastructure Features

- 🔐 Firebase JWT Authentication
- ⚡ Taskiq + Redis Async Tasks
- 🧠 InjectQ Dependency Injection
- 📊 Prometheus Metrics
- 🚨 Sentry Error Tracking
- 🐳 Docker Compose Orchestration
- 🧪 60+ Automated Tests
- 🚀 GitHub Actions CI/CD

---

# 🏛️ Architecture Overview

```text
                        ┌──────────────────────┐
                        │ Firebase JWT Auth   │
                        └──────────┬───────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      FastAPI Backend        │
                    │   Uvicorn + InjectQ + DI    │
                    └───────┬─────────┬───────────┘
                            │         │
             ┌──────────────┘         └──────────────┐
             ▼                                       ▼

      ┌──────────────┐                     ┌────────────────┐
      │ PostgreSQL   │                     │ MongoDB        │
      │ Relational   │                     │ Document DB    │
      └──────────────┘                     └────────────────┘

                           ┌────────────────┐
                           │ Neo4j Graph DB │
                           └────────────────┘
```

---

# 🐘 PostgreSQL — Relational Database

## Features

- Normalized schema design
- Strong data integrity
- SQL analytical queries
- Composite indexing
- Relational joins

---

## APIs

| Endpoint | Description |
|---|---|
| `POST /api/oltp/init` | Initialize relational database |
| `GET /api/oltp/customers-with-purchases` | Customer purchase history |
| `GET /api/oltp/top-products` | Top-selling products |
| `GET /api/oltp/recommendations/{id}` | Product recommendations |

---

# 🍃 MongoDB — Document Database

## Features

- Embedded recent purchases
- Aggregation pipelines
- Flexible schemas
- Dynamic category attributes
- Fast customer profile retrieval

---

## APIs

| Endpoint | Description |
|---|---|
| `POST /api/nosql/init` | Initialize MongoDB |
| `GET /api/nosql/customers` | Customer documents |
| `GET /api/nosql/products/{category}` | Filter products |
| `GET /api/nosql/purchases/{email}` | Purchases by email |

---

# 🔮 Neo4j — Graph Database

## Features

- Graph-based recommendations
- Relationship traversal
- Collaborative filtering
- Product recommendation engine

---

## APIs

| Endpoint | Description |
|---|---|
| `POST /api/graph/init` | Initialize graph database |
| `GET /api/graph/recommendations/{name}` | Graph recommendations |
| `GET /api/graph/customer-history/{email}` | Customer history |
| `GET /api/graph/top-products` | Top graph products |

---

# ⚡ Quick Start

# 🐳 Docker Setup (Recommended)

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-org/backend-base.git

cd backend-base
```

---

## 2️⃣ Configure Environment

```bash
cp .env.example .env
```

---

## 3️⃣ Start All Services

```bash
docker compose -f docker/docker-compose.yml up -d
```

---

# 🌐 Service URLs

| Service | URL |
|---|---|
| FastAPI | http://localhost:8082 |
| Swagger Docs | http://localhost:8082/docs |
| ReDoc | http://localhost:8082/redocs |
| Neo4j Browser | http://localhost:7474 |
| PostgreSQL | localhost:5432 |
| MongoDB | localhost:27017 |
| Jupyter Lab | http://localhost:8888 |

---

# 🧪 Database Initialization

## PostgreSQL

```bash
curl -X POST http://localhost:8082/api/oltp/init
```

---

## MongoDB

```bash
curl -X POST http://localhost:8082/api/nosql/init
```

---

## Neo4j

```bash
curl -X POST http://localhost:8082/api/graph/init
```

---

# 💻 Local Development Setup

## Create Virtual Environment

### Linux / Mac

```bash
python -m venv .venv

source .venv/bin/activate
```

---

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r docker/requirements.txt
```

---

# Run Application

```bash
uvicorn src.app.main:app --reload --host localhost --port 8082
```

---

# 📁 Project Structure

```text
backend-base/
│
├── src/
│   ├── app/
│   ├── routers/
│   ├── db/
│   ├── tasks/
│   ├── utils/
│   └── tests/
│
├── docker/
├── scripts/
├── notebooks/
├── .github/
└── README.md
```

---

# 🧪 Testing

# Run All Tests

```bash
pytest
```

---

# Run Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

---

# Run Ruff Linter

```bash
ruff check src/
```

---

# Run MyPy

```bash
mypy src/
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| Relational Database | PostgreSQL |
| Document Database | MongoDB |
| Graph Database | Neo4j |
| ORM | Tortoise ORM |
| Authentication | Firebase |
| Queue System | Redis + Taskiq |
| Dependency Injection | InjectQ |
| Monitoring | Sentry |
| Metrics | Prometheus |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

# 🔐 Authentication

All APIs require Firebase JWT Bearer Token.

## Example

```http
Authorization: Bearer <your_token>
```

---

# ⚡ Background Tasks

Taskiq + Redis are used for async task processing.

## Start Worker

```bash
taskiq worker src.app.worker:broker -fsd -tp "src/**/*_tasks.py" --reload
```

---

# 📊 CI/CD Pipeline

```text
PR → Pre-commit → Ruff → Pytest → Coverage → Merge
```

---

# 🚢 Docker Services

```yaml
services:
  postgres:
  mongodb:
  neo4j:
  redis:
  base_app:
  jupyter:
```

---

# 📈 Database Comparison

| Feature | PostgreSQL | MongoDB | Neo4j |
|---|---|---|---|
| Schema | Strict | Flexible | Graph |
| Relationships | JOINs | Embedded Docs | Relationships |
| Recommendations | SQL Logic | Aggregation | Graph Traversal |
| Scaling | Vertical | Horizontal | Relationship-heavy |

---

# ❤️ Why This Project Is Special

This project demonstrates how modern backend systems can combine:

- Relational databases
- Document databases
- Graph databases
- Authentication
- Async processing
- Monitoring
- Metrics
- CI/CD
- Containerization

inside one scalable FastAPI architecture.

---

# 📝 License

MIT License

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository  
🍴 Fork the project  
🚀 Build something awesome  

---

<div align="center">

# ❤️ Built For Curious Backend Developers

### FastAPI • PostgreSQL • MongoDB • Neo4j • Docker

</div>
