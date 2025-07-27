

## What is APIRouter?
APIRouter is a class provided by FastAPI to help modularize your routes.

Instead of defining all endpoints in the main app, you can:
* Create routers for different features or modules (e.g., users, items).
* Group related routes together.
* Apply common dependencies, prefixes, or tags to a group of routes.


### Grouping Routes with Routers
FastAPI provides APIRouter to modularize routes.

```bash
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return [{"user_id": 1, "name": "John"}]

@router.post("/users")
def create_user(user: dict):
    return {"message": "User created", "user": user}

# Include the users group of routes
app.include_router(router, prefix="/api")
```
* The prefix argument adds a common prefix to all routes in the router.





