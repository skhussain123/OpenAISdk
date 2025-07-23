


### 1. Get Url
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{id}")
def read_root(id: int):
 
    return{
        'status': 'success',
        'data': {
            "id": id,
        }
    }  
```


### 2. post Request
```bash

from pydantic import BaseModel

class PostData(BaseModel):
    name: str
    email: str


@app.post("/user-form/")
def read_root(postdata:PostData):
 
    return{
        'status': 'success',
        'data': {
            "ss": postdata,
        }
    }
```    
    
* http://127.0.0.1:8000/user-form/
* post 
* body --> raw --> json 
```bash
{
    "name": "hussain",
    "email": "hk0527075@gmail.com"
}
``` 

### 3. update Request
```bash
app = FastAPI()

class PostData(BaseModel):
    name: str
    email: str

@app.put("/user-form/{id}")
def update_user(id: int, postdata: PostData):
    return {
        'status': 'success',
        'message': f'User with id {id} updated successfully',
        'data': {
            "id": id,
            "name": postdata.name,
            "email": postdata.email
        }
    }
```
* URL: http://127.0.0.1:8000/user-form/1
* Method: PUT
* Body (raw → JSON)
```bash
{
    "name": "Hussain Updated",
    "email": "hussain_updated@example.com"
}
```

### 4. Delete Request
```bash
@app.delete("/user-form/{id}")
def delete_user(id: int):
    return {
        'status': 'success',
        'message': f'User with id {id} deleted successfully'
    }
```
* URL: http://127.0.0.1:8000/user-form/1
* Method : DELETE


