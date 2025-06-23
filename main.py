from fastapi import FastAPI
from database import engine
from models import Base
from routes import blog
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)


