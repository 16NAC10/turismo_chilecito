from fastapi import FastAPI
from services.osm_service import fetch_osm_data
from services.normalize import normalize_osm_element
from models.opinion import Opinion
from dao.opinion_dao import (
    create_opinion,
    get_by_lugar,
    get_promedio_por_lugar
)
from models.lugar import Lugar
from dao.lugar_dao import (
    create_lugar,
    get_all,
    update_lugar,
    delete_lugar,
    get_by_tipo_nombre,
    get_by_categoria_nombre
)
from models.servicio import Servicio
from dao.servicio_dao import get_or_create_servicio, get_all_services
from models.tipo import Tipo
from dao.tipo_dao import get_or_create_tipo, get_all_tipos
from models.categoria import Categoria
from dao.categoria_dao import get_or_create_categoria, get_all_categorias, get_by_nombre

app = FastAPI()

@app.post("/import-osm")
def import_osm():
    data = fetch_osm_data()
    for el in data:
        lugar = normalize_osm_element(el)
        create_lugar(lugar)
    return {"importados": len(data)}

@app.post("/lugares/new")
def nuevo(lugar: dict):
    lugar["osm_id"] = None
    create_lugar(lugar)
    return {"ok": True}

@app.get("/lugares")
def listar():
    return get_all()

@app.get("/lugares/tipo/{tipo_nombre}")
def lugares_por_tipo(tipo_nombre: str):
    return get_by_tipo_nombre(tipo_nombre)

@app.get("/lugares/categoria/{categoria_nombre}")
def lugares_por_categoria(categoria_nombre: str):
    return get_by_categoria_nombre(categoria_nombre)

@app.put("/lugares/{id}")
def modificar(id: int, data: dict):
    update_lugar(id, data)
    return {"ok": True}

@app.delete("/lugares/{id}")
def borrar(id: int):
    delete_lugar(id)
    return {"ok": True}

@app.get("/tipos")
def listar():
    return get_all_tipos()

@app.get("/categorias")
def listar():
    return get_all_categorias()

@app.post("/opiniones")
def nueva_opinion(opinion: Opinion):
    create_opinion(opinion.dict())
    return {"ok": True}

@app.get("/opiniones/lugar/{lugar_id}")
def opiniones_por_lugar(lugar_id: int):
    return get_by_lugar(lugar_id)

@app.get("/opiniones/promedios")
def promedios():
    return get_promedio_por_lugar()

@app.post("/servicios")
def nuevo_servicio(service: Servicio):
    create_service(service.dict())
    return {"ok": True}

@app.get("/servicios")
def listar_servicios():
    return get_all_services()

@app.get("/lugares/{id}/servicios")
def servicios_de_lugar(id: int):
    return get_servicios_by_lugar(id)

@app.delete("/lugares/{lugar_id}/servicios/{servicio_id}")
def quitar_servicio(lugar_id: int, servicio_id: int):
    delete_service_from_lugar(lugar_id, servicio_id)
    return {"ok": True}