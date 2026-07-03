# FastAPI training exercise n.1

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return {'Message:': 'Hello World'}