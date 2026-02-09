from pydantic import BaseModel

class Tipo(BaseModel):
    id_tipo: str
    nombre: str
    categoria_id: str