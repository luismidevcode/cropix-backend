from fastapi import FastAPI
from Backend.routers import varieties
from routers import users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers

app.include_router(users.router)
app.include_router(varieties.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/ventas")
async def ventas():
    return {"Ventas": "Pantalla de Ventas"}

