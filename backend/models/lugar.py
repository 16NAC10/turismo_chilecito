from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class Lugar(BaseModel):
    id: str
    nombre: str = Field(..., min_length=2, max_length=120)
    tipo_id: str
    servicios_ids: List[str] = []
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    source: Literal["OSM", "MANUAL"]

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        return v