from pydantic import BaseModel
from typing import Optional, Dict

class Location(BaseModel):
    name: Optional[str]
    category: str
    osm_type: str
    tags: Dict
    lat: float
    lon: float
