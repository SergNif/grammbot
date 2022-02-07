from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def index():
    """
    A simple Hello World GET request
    """
    return {"message": "Hello, World!"}

if __name__ == '__main__':
    uvicorn.run('asgi:app', host='0.0.0.0',  reload = True)