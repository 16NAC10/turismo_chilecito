from pydantic import BaseModel, Field


class Servicio(BaseModel):
    id_servicio: str
    nombre: str = Field(..., min_length=2, max_length=80)
    descripcion: str | None = None