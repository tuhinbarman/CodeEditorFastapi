from fastapi import FastAPI
from database import Base,engine
import models
from routers import rooms

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rooms.router,prefix='')



