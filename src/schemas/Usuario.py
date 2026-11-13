#Esquemas Pydantic de usuarios (peticiones y respuestas de la API)
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

from models.Usuario import Usuario


class UsuarioCreate(BaseModel):
    #Datos que envía el cliente para crear un usuario
    nombre: str = Field(..., min_length=1, examples=["Ana García"])
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", examples=["ana@mail.com"])
    tipo: Literal["cliente", "administrador"] = Field(..., examples=["cliente"])
    direccion: Optional[str] = Field(None, examples=["C/ Mayor 1, Madrid"])

    @model_validator(mode="after")
    def comprobar_direccion(self) -> "UsuarioCreate":
        #Un cliente necesita dirección postal
        if self.tipo == "cliente" and not self.direccion:
            raise ValueError("Un cliente necesita una dirección postal.")
        return self


class UsuarioRead(BaseModel):
    #Datos del usuario que se devuelven al cliente
    id: str
    nombre: str
    email: str
    es_admin: bool

    @classmethod
    def desde_modelo(cls, usuario: Usuario) -> "UsuarioRead":
        #Convierte un objeto Usuario del dominio en el esquema de salida
        return cls(id=usuario.id, nombre=usuario.nombre,
                   email=usuario.email, es_admin=usuario.is_admin())
