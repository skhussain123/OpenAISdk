

### Front to Backend data transfer With Get Request
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


### Query Perameter 
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


### Send data With post request in Body
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