from pydantic import BaseModel

class Categoria(BaseModel):
    id_categoria: int
    nombre: str