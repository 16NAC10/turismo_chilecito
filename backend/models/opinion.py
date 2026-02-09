from pydantic import BaseModel, Field
from typing import Optional

class Opinion(BaseModel):
    id_opinion: Optional[str] = None
    lugar_id: str
    puntuacion: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None