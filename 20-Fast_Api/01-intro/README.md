

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
uvicorn main:app --reload
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
