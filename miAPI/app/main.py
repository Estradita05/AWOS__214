from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional


app= FastAPI(
    title="Mi primer API",
    description="Esta es mi primera API con FastAPI en la clase del profe Isay",
    version="1.0.0"
    )

#TB ficticia
usuarios=[
    {"id":1, "nombre":"Montse", "edad": 20},
    {"id":2, "nombre":"Karla", "edad": 19},
    {"id":3, "nombre":"Pilar", "edad": 19},
]

#Endpoint
@app.get("/", tags=["Inicio"]) 
async def bienvenida():
    return {"message": "Bienvenido a mi API"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"]) #Endpoint
async def hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola Mundo FAstAPI" ,
            "estatus" : "200"
            } #formato json

@app.get("/v1/parametroOb/{id}" ,tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario" : id }

@app.get("/v1/parametroOp/" ,tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}
        return {"mensaje": "Usuario no encontrado"}
    return {"mensaje": "usuario no encontrado" , "usuario":id}

@app.get("/v1/usuarios/" ,tags=['CRUD HTTP'])
async def leer_usuarios( ):
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/" ,tags=['CRUD HTTP'])
async def crear_usuario(usuario:dict):
    raise HTTPException(
        status_code=400,
        detail="El id ya existe"
    )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }

@app.put("/v1/usuarios/{id}" ,tags=['CRUD HTTP'])
async def actualizar_usuario(id:int, usuario:dict):
    for i, u in enumerate(usuarios):
        if u["id"] == id:
            usuarios[i] = usuario
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}" ,tags=['CRUD HTTP'])
async def eliminar_usuario(id:int):
    for i, u in enumerate(usuarios):
        if u["id"] == id:
            usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )