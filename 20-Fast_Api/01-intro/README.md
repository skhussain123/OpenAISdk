
### Intro
FastAPI lets you create web APIs in Python — just like Django or Flask, but faster and smarter.

### FastApi Work

#### 1. Frontend (e.g., React, Angular, HTML/JS)
User koi action karta hai — jaise form submit ya button click.

#### 2. Request to FastAPI
Frontend se HTTP request jaata hai (like GET, POST, etc.) FastAPI ke server pe.

#### 3. FastAPI (Backend)

* Request ko process karta hai
* Database se data leta hai (agar zarurat ho)
* Response banata hai

#### 4. Response to Frontend
FastAPI ye response JSON format me frontend ko wapas bhej deta hai.

```bash
[Frontend UI]
     ↓  (Request)
[FastAPI Server]
     ↓  (Fetch from DB, Logic)
[FastAPI Server]
     ↑  (JSON Response)
[Frontend UI]

```

### Install FastApi
```bash
uv add fastapi uvicorn 
```

### Fastapi Run project 
```bash
uvicorn main:app --reload
```

### Fastapi Run project with Different Port
```bash
uvicorn main:app --reload --port 5000
```


## Intro


### Swagger UI

* Ek interactive documentation hoti hai.
* Aap directly API ko test kar sakte ho — jaise GET, POST requests bhejna.
* Developer-friendly aur fast debugging ke liye useful.

```bash
http://127.0.0.1:8000/docs
```

### ReDoc

* Ek read-only style documentation hai — clean aur structured.
* Mainly API ke overview and structure ke liye useful hoti hai.
* Interactive nahi hoti jaise Swagger, lekin visually zyada clean hoti hai.
```bash
http://127.0.0.1:8000/redoc
```

### Comparison
| Feature             | Swagger UI    | ReDoc             |
| ------------------- | ------------- | ----------------- |
| Interactive Try     | ✅ Yes         | ❌ No              |
| Clean UI            | ⚠️ OK         | ✅ Very Clean      |
| Built-in in FastAPI | ✅ Yes         | ✅ Yes             |
| For Testing         | ✅ Best suited | ❌ Not for testing |


### main.py ('Hello World')
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```    