from pydantic import BaseModel

class Categoria(BaseModel):
    id_categoria: str
    nombre: str