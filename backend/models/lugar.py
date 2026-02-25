from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

from models.servicio import Servicio
from models.tipo import Tipo


class Lugar(BaseModel):
    id: str
    nombre: str
    lat: float
    lon: float
    tipo: Tipo
    servicios: list[Servicio] = []
    source: str
    osm: dict | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v