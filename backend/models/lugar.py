from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Lugar(BaseModel):
    id: str
    nombre: Optional[str] = None
    tipo: str
    categoria: str
    servicios: List[str] = []
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    source: Literal["OSM", "MANUAL"]