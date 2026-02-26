from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

app = FastAPI()

# Base de datos en memoria
libros = []
prestamos = []

# Año actual
anio_actual = datetime.now().year


# MODELOS PYDANTIC

class Libro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str
    anio: int = Field(gt=1450, le=anio_actual)
    paginas: int = Field(gt=1)
    estado: str

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario


# ENDPOINTS

# Registrar libro
@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    if libro.estado not in ["disponible", "prestado"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    for l in libros:
        if l["nombre"] == libro.nombre:
            raise HTTPException(status_code=400, detail="Libro ya registrado")

    libros.append(libro.dict())
    return {"mensaje": "Libro registrado correctamente"}


# Listar libros
@app.get("/libros")
def listar_libros():
    return libros


# Buscar libro por nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in libros:
        if libro["nombre"] == nombre:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


# Registrar préstamo
@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["nombre"] == prestamo.nombre_libro:

            if libro["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="Libro ya prestado")

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Préstamo registrado"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# Devolver libro
@app.put("/prestamos/devolver/{nombre}")
def devolver_libro(nombre: str):

    for prestamo in prestamos:
        if prestamo["nombre_libro"] == nombre:

            for libro in libros:
                if libro["nombre"] == nombre:
                    libro["estado"] = "disponible"

            prestamos.remove(prestamo)
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(status_code=409, detail="El préstamo no existe")


# Eliminar préstamo
@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):

    for prestamo in prestamos:
        if prestamo["nombre_libro"] == nombre:
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}

    raise HTTPException(status_code=409, detail="El préstamo no existe")