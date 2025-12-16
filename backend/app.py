from fastapi import FastAPI
from services.osm_service import fetch_osm_data
from services.normalize import normalize_osm_element
from dao.location_dao import (
    create_location,
    get_all,
    get_by_tipo,
    update_location,
    delete_location
)

app = FastAPI()

@app.post("/import-osm")
def import_osm():
    data = fetch_osm_data()
    for el in data:
        loc = normalize_osm_element(el)
        create_location(loc)
    return {"importados": len(data)}

@app.post("/lugares/new")
def nuevo(location: dict):
    create_location(location)
    return {"ok": True}

@app.get("/lugares")
def listar():
    return get_all()

@app.get("/lugares/tipo/{tipo}")
def listar_por_tipo(tipo: str):
    return get_by_tipo(tipo)

@app.put("/lugares/{id}")
def modificar(id: int, data: dict):
    update_location(id, data)
    return {"ok": True}

@app.delete("/lugares/{id}")
def borrar(id: int):
    delete_location(id)
    return {"ok": True}
