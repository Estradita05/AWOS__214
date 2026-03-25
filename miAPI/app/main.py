from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import Base, engine
from app.models import usuario

Base.metadata.create_all(bind=engine)

#Instancia del servidor
app= FastAPI(
    title="Mi primer API",
    description="Esta es mi primera API con FastAPI en la clase del profe Isay",
    version="1.0.0"
    )

app.include_router(usuarios.router)
app.include_router(varios.router)





