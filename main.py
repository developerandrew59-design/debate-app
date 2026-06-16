from fastapi import FastAPI
import models
from database import engine
from routers import users,clubs,arguments


app=FastAPI()

#models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(clubs.router)
app.include_router(arguments.router)


@app.get("/")
def start():
    return {"message":"something has gotta be wrong"}