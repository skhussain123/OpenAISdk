

#### Type of perameter 
* path peramter
* query Perameter
* body perameter

### 1. Front to Backend data transfer With Get Request  (path peramter)
```bash
app = FastAPI()

@app.get("/user/{id}/{name}")

def read_root(id:int,name:str):
        return{
            'status': 'success',
            'data':{
                'id': id,
                'name':name,
                'profile':'url here',
                'age': 25,
                'address':'karachi'
            }

        }
```
* you Need to pass id in Parameters from Fastapi docs then excute        


### 2. Query Perameter  
```bash
app = FastAPI()

@app.get("/user")

def read_root(id:int,name:str,age: int):
        return{
            'status': 'success',
            'data':{
                'id': id,
                'name':name,
                'profile':'url here',
                'age': age,
                'address':'karachi'
            }

        }
```
* if you send request using postman you will see the make url is this http://127.0.0.1:8000/user?id=222&name=hussain&profile=dfsdfs&age=33&address=kaarchi


### 3. Send data With post request (body peramter)
```bash
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

// this is a pydentic model jo ye sure kryga ke front sy(postman or frontend) body me jo data aeyga usmy ye kesy value hongi 
class Person(BaseModel):
    id : int
    name: str
    age: int
    email: str


@app.post("/user")
def read_root(person:Person):
    
    try:
        return{
            'status': 'success',
            'data': person

        }
        
    except Exception as e:
        return{
            'status': 'error',
            'data': str(e)

        }
```
* POST
* http://127.0.0.1:8000/user
* post url test api url 
* row --> json --> 
```bash
{
    "id":222,
    "name":"hussain",
    "age":21,
    "email": "hussain123@gmail.com"

}
```
* output
```bash
{
    "status": "success",
    "data": {
        "id": 222,
        "name": "hussain",
        "age": 21,
        "email": "hussain123@gmail.com"
    }
}
```

### 4. Path Perameter , Query Perameter , Body Perameter (All With)
```bash
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    id : int
    name: str
    age: int
    email: str


@app.post("/user/{id}")
def read_root(id :int,query:str,person:Person):
    
    try:
        return{
            'status': 'success',
            'data': {
                'person': person,
                "id": id,
                "query":query
            }

        }
        
    except Exception as e:
        return{
            'status': 'error',
            'data': str(e)

        }
```
* http://127.0.0.1:8000/user/33/?query=search here
* post 
* row --> json --> 
```bash
{
    "id":222,
    "name":"hussain",
    "age":21,
    "email": "hussain123@gmail.com"

}
```
* output
```bash
{
    "status": "success",
    "data": {
        "person": {
            "id": 222,
            "name": "hussain",
            "age": 21,
            "email": "hussain123@gmail.com"
        },
        "id": 33,
        "query": "search here"
    }
}
```


### 5. Perameter Validation
```bash
def read_root(id: int, person: Person, query: Optional[str] = None):  // optional perameter last me dena hain
```

```bash
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Person(BaseModel):
    id : int
    name: Optional[str] = None
    age: int
    email: str
    address: Optional[str] = None


@app.post("/user/{id}")
def read_root(id: int, person: Person, query: Optional[str] = None):
    
    try:
        return{
            'status': 'success',
            'data': {
                'person': person,
                "id": id,
                "query":query
            }

        }
        
    except Exception as e:
        return{
            'status': 'error',
            'data': str(e)

        }
```

### 6. Perameter Condition
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/user/{id}")
def read_root(id: int):
    
    try:
        if id < 100:
            raise ValueError('id Should be greater than 100')
        
        return{
            'status': 'success',
            'data': {
                "id": id,
                }
            }
        
    except Exception as e:
        return{
            'status': 'error',
            'data': str(e)

        }
```
 





