

### Front to Backend data transfer
```bash
app = FastAPI()

@app.get("/user/{id}")

def read_root(id):
        return{
            'status': 'success',
            'data':{
                'id': id,
                'name':'husain',
                'profile':'url here',
                'age': 25,
                'address':'karachi'
            }

        }
```
* you Need to pass id in Parameters from Fastapi docs then excute        