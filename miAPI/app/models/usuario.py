#Modelo de validicion Pydantic}
from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max=50, example="Isaac")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")

