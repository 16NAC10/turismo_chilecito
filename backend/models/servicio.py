from pydantic import BaseModel

class Servicio(BaseModel):
    id_servicio: int
    nombre: str