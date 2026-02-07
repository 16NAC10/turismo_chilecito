from pydantic import BaseModel, conint
from typing import Optional

class Opinion(BaseModel):
    id_opinion: int
    lugar_id: int
    puntuacion: conint(ge=1, le=5)
    comentario: Optional[str] = None