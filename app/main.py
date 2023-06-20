from fastapi import FastAPI
from typing import List
from models import *


app = FastAPI()

@app.get("/ports", response_model=List[Port])
def get_ports():
    ports = [
        Port(id=1, value='COM1'),
        Port(id=2, value='COM2'),
        Port(id=3, value='COM3'),
        Port(id=4, value='COM4')
    ]
    return ports

# Определите аналогичные пути для остальных методов


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
