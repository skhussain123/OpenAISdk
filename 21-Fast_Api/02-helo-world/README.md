

#### 
```bash
app = FastAPI(title="fast api")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# @app.push("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}


@app.delete("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.put("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```   

#### Fastapi Run project 
```bash
uvicorn main:app --reload
```

#### Fastapi Run project with Different Port
```bash
uvicorn main:app --reload --port 5000
```

#### Api Test
```bash
http://127.0.0.1:8000/docs
```


### What is an Endpoint in Web Development?
An endpoint is a URL path that a client (like frontend, mobile app, or Postman) can send a request to and get a response from the backend (e.g., FastAPI server).

#### Simple Request
```bash
@app.get("/users")
def get_users():
    return {"message": "List of users"}

```

#### With Send Data
```bash
@app.get("/")
def read_root():
    return {
        "data": ['hussain','ali'],
        "message": "Hello, FastAPI!",
        "status":200
        }
     
```

#### With Try Catch
```bash
app = FastAPI()

@app.get("/")
def read_root():
    try:
        
        return{
            'status': 'success',
            'data':{
                'name':'husain',
                'profile':'url here',
                'age': 25,
                'address':'karachi'
            }

        }
        
    except Exception as e: 
        return {
        "message": str(e),
        "error":404
        }
```        


* /users is the endpoint
* GET is the method
* When someone visits http://127.0.0.1:8000/users, they are hitting that endpoint


| Method | Use Case             | Example Endpoint      |
| ------ | -------------------- | --------------------- |
| GET    | Read data            | `/users`, `/products` |
| POST   | Create new data      | `/users`, `/login`    |
| PUT    | Update existing data | `/users/5`            |
| DELETE | Delete data          | `/users/5`            |


### base endpoint
* base endpoint wo hota ha jo kabhi change nh hota. like http://127.0.0.1
* 8000 --> qk port hum change kr sakty hain ha lekin main url change nh kr sakty.
*  /users --> qk perameter hum change kr sakty hain ha lekin main url change nh kr sakty.