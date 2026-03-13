from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import List
import secrets

app = FastAPI(title="API Sistema de Tickets")

security = HTTPBasic()

# Credenciales
USERNAME = "soporte"
PASSWORD = "4321"

# AUTENTICACIÓN
def verificar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    correcto_usuario = secrets.compare_digest(credentials.username, USERNAME)
    correcto_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correcto_usuario and correcto_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# MODELO
class Ticket(BaseModel):
    nombre_usuario: str = Field(..., min_length=5)
    descripcion_problema: str = Field(..., min_length=20, max_length=200)
    prioridad: str = Field(..., pattern="^(baja|media|alta)$")
    estado: str = "pendiente"

# Base de datos temporal
tickets = []
contador_id = 1


# CREAR TICKET 
@app.post("/tickets", tags=["Tickets"])
def crear_ticket(ticket: Ticket):
    global contador_id

    nuevo_ticket = ticket.dict()
    nuevo_ticket["id"] = contador_id

    tickets.append(nuevo_ticket)
    contador_id += 1

    return {"mensaje": "Ticket creado", "ticket": nuevo_ticket}

# LISTAR TICKETS 
@app.get("/tickets", tags=["Tickets"])
def listar_tickets():
    return tickets


# CONSULTAR POR ID 
@app.get("/tickets/{ticket_id}", tags=["Tickets"])
def consultar_ticket(ticket_id: int, usuario: str = Depends(verificar_usuario)):

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise HTTPException(status_code=404, detail="Ticket no encontrado")


# CAMBIAR ESTADO 
@app.put("/tickets/{ticket_id}/estado", tags=["Tickets"])
def cambiar_estado(ticket_id: int, nuevo_estado: str, usuario: str = Depends(verificar_usuario)):

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["estado"] = nuevo_estado
            return {"mensaje": "Estado actualizado", "ticket": ticket}

    raise HTTPException(status_code=404, detail="Ticket no encontrado")


# ELIMINAR TICKET 
@app.delete("/tickets/{ticket_id}", tags=["Tickets"])
def eliminar_ticket(ticket_id: int):

    for ticket in tickets:
        if ticket["id"] == ticket_id:

            if ticket["estado"] == "resuelto":
                raise HTTPException(
                    status_code=400,
                    detail="No es posible eliminar tickets resueltos"
                )

            tickets.remove(ticket)
            return {"mensaje": "Ticket eliminado con exito"}

    raise HTTPException(status_code=404, detail="Ticket no encontrado")