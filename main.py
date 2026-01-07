from fastapi import FastAPI
from routers import news, users
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(news.router)