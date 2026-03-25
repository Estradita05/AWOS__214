from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.models.usuario import Usuario
from app.security.auth import verificar_Peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

@router.get("/")
def leer_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(nombre: str, edad: int, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(nombre=nombre, edad=edad)

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario agregado",
        "usuario": nuevo_usuario
    }

@router.put("/{id}")
def actualizar_usuario(id: int, nombre: str, edad: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = nombre
    usuario.edad = edad

    db.commit()

    return {
        "mensaje": "Usuario actualizado",
        "usuario": usuario
    }

@router.delete("/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db), userAuth: str = Depends(verificar_Peticion)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por: {userAuth}"
    }