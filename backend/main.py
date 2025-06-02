from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/feature")
async def feature():
    return {"feature-message": "This is a feature message"}