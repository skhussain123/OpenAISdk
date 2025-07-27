

## 1. What is APIRouter?
APIRouter is a class provided by FastAPI to help modularize your routes.

Instead of defining all endpoints in the main app, you can:
* Create routers for different features or modules (e.g., users, items).
* Group related routes together.
* Apply common dependencies, prefixes, or tags to a group of routes.


* Swagger openai ke name pr kam krta ha.
* fast api openai ka standart ka use krke json sepcification khud se bana deta ha or swagger uska use krke
ui bana deta hun jaha hum api test kr sakty hain. jasy swagger doc bhi kaha jata ha

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


## 2. Route Dependencies
* Dependencies can be added to routes to perform shared logic.

```bash
from fastapi import Depends

def common_dependency():
    return {"key": "value"}

@app.get("/items")
def read_items(data: dict = Depends(common_dependency)):
    return data
```

## 3. Middleware and Route Preprocessing
* Middleware can intercept requests/responses before they reach the route.
```bash
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Bydefault Created Middleware for read_root 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all (ip,domain,server)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware for read_root 
@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("request",request)
    print("call_next",call_next)
    response = await call_next(request)
    response.headers["X-Process-Time"] = "10 sec"
    return response

@app.get("/")
def read_root():
    return {"message": "server is running"}

    
@app.get("/abc")
def abc_root():
    return {"message": "abc"}
```    

## 4. Handling Async Endpoints
```bash
import asyncio

@app.get("/async")
async def read_async():
    await asyncio.sleep(1)
    return {"message": "This is asynchronous!"}
```   

#### await
Agar async function ke andar koi aisa kaam hai jisko complete hone mein time lagta hai (jaise: database call, API request, file read/write), to uske aage await lagate hain.
await ka matlab hota hai: "Wait karo is kaam ke complete hone tak, phir aage badho."

#### async
Jab aap kisi function ko asynchronous banana chahte hain (matlab wo function background mein kaam kare aur dusre kaam rukke bina chale), to us function ke aage async likhte hain.

#### Synchronous: Ek waiter ek table ka order leta hai, jab tak wo order pura nahi hota, dusra table wait karta hai.

####  Asynchronous: Ek waiter order leke kitchen mein bhejta hai (background mein process hota hai), tab tak wo dusre table pe kaam karta rehta hai.





