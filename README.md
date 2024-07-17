# FastAPI Starter

# Used Libraries



# DB Migration
aerich init -t app.db.TORTOISE_ORM



To run this app
```
uvicorn app.main:app --reload
```

Vscode config
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app", "--reload"
            ],
            "jinja": true
        }
    ]
}
```
