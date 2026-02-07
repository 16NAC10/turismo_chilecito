from pydantic import BaseModel

class Tipo(BaseModel):
    id_tipo: int
    nombre: str