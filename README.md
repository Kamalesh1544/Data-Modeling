
# Project Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Database](#database)
   - [Configuration](#database-configuration)
   - [Migration](#database-migration)
5. [Running the Application](#running-the-application)
   - [Command Line](#command-line)
   - [VS Code](#vs-code)
6. [Development](#development)
   - [Pre-commit Hooks](#pre-commit-hooks)
   - [Code Style](#code-style)
7. [API Documentation](#api-documentation)
8. [Testing](#testing)


## Introduction
[Provide a brief introduction to your project, its purpose, and main features.]

## Project Structure
```
project_root/
├── src/
│   └── app/
│       ├── main.py
│       └── db/
│           └── setup_database.py
├── tests/
├── requirements.txt
├── .pre-commit-config.yaml
└── README.md
```

## Setup

### Prerequisites
- Python 3.x
- pip
- [Any other prerequisites]

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/10XScale-in/backend-base.git
    ```

2. Create a virtual environment and activate:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Database

### Database Configuration
The database configuration is located in `src/app/db/setup_database.py`.

### Database Migration
We use Aerich for database migrations. Follow these steps to manage your database:

1. Initialize the database initially:
    ```bash
    aerich init -t src.app.db.setup_database.TORTOISE_ORM
    ```

2. Create initial database schema:
    ```bash
    aerich init-db
    ```

3. Generate migration files:
    ```bash
    aerich migrate
    ```

4. Apply migrations:
    ```bash
    aerich upgrade
    ```

5. Revert migrations (if needed):
    ```bash
    aerich downgrade
    ```

## Running the Application

### Command Line
To run the FastAPI application using Uvicorn:
1. Start the application:
    ```bash
    uvicorn src.app.main:app --reload
    ```

2. You can also run the debugger.

### VS Code
Add the following configuration to your `.vscode/launch.json` file:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.app.main:app",
                "--host",
                "localhost",
                "--port",
                "8880"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
Then you can run and debug the application using the VS Code debugger.

## Development

### Pre-commit Hooks
We use pre-commit hooks to ensure code quality. To set them up:

1. Install the pre-commit package:
    ```bash
    pip install pre-commit
    ```

2. Install the git hook scripts:
    ```bash
    pre-commit install
    ```

### Code Style
    1.ruff,
    2.mypy,
    3.bandit

## Testing
 1.pytest
