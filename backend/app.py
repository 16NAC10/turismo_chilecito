import uuid

from fastapi import FastAPI
from fastapi import HTTPException

from models.servicio import Servicio
from services.osm_service import fetch_osm_data
from services.normalize import normalize_osm_element
from models.opinion import Opinion
from dao.opinion_dao import (
    create_opinion,
    get_by_lugar,
    delete_opinion, get_promedio_by_lugar
)
from dao.lugar_dao import (
    create_lugar,
    get_all,
    update_lugar,
    delete_lugar,
    get_by_tipo,
    get_by_categoria, get_lugar, get_by_servicio, lugares, add_servicio, remove_servicio, exists_lugar
)
from dao.servicio_dao import get_by_id, create_servicio, get_all_servicios, delete_servicio
from dao.tipo_dao import get_all_tipos, create_tipo, update_tipo, delete_tipo
from dao.categoria_dao import get_all_categorias, create_categoria, update_categoria, \
    delete_categoria

app = FastAPI()


@app.post("/import-osm")
def import_osm():
    data = fetch_osm_data()
    for el in data:
        lugar = normalize_osm_element(el)
        create_lugar(lugar)
    return {"importados": len(data)}


@app.post("/lugares/new")
def crear_lugar(lugar: dict):
    lugar["osm_id"] = None
    lugar["source"] = "MANUAL"
    lugar["servicios"] = lugar.get("servicios", [])

    create_lugar(lugar)
    return {"ok": True, "message": "Lugar creado correctamente"}


@app.get("/lugares/{lugar_id}")
def obtener_lugar(lugar_id: str):
    lugar = get_lugar(lugar_id)

    if not lugar:
        raise HTTPException(
            status_code=404,
            detail="Lugar no encontrado"
        )

    return lugar


@app.put("/lugares/{lugar_id}")
def modificar_lugar(lugar_id: str, data: dict):
    actualizado = update_lugar(lugar_id, data)

    if not actualizado:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    return {"Lugar modificado correctamente": True}


@app.delete("/lugares/{id}")
def borrar_lugar(id: str):
    borrado = delete_lugar(id)

    if not borrado:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    return {"Lugar borrado": True}


@app.get("/lugares")
def listar_lugares():
    return get_all()


@app.get("/lugares/tipo/{tipo_nombre}")
def lugares_por_tipo(tipo_nombre: str):
    return get_by_tipo(tipo_nombre)


@app.get("/lugares/categoria/{categoria_nombre}")
def lugares_por_categoria(categoria_nombre: str):
    return get_by_categoria(categoria_nombre)


@app.post("/tipos/new")
def crear_tipo(data: dict):
    try:
        tipo_id = create_tipo(
            data.get("nombre"),
            data.get("categoria_nombre")
        )
        return {"Tipo creado correctamente": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/tipos/{tipo_id}")
def modificar_tipo(tipo_id: str, data: dict):
    try:
        actualizado = update_tipo(tipo_id, data)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")
        return {"Tipo modificado correctamente": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/tipos/{tipo_id}")
def borrar_tipo(tipo_id: str):
    try:
        eliminado = delete_tipo(tipo_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/tipos")
def listar_tipos():
    return get_all_tipos()


@app.post("/categorias/new")
def crear_categoria(data: dict):
    try:
        categoria_id = create_categoria(data.get("nombre", ""))
        return {"id": categoria_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/categorias/{categoria_id}")
def modificar_categoria(categoria_id: str, data: dict):
    try:
        ok = update_categoria(categoria_id, data)
        if not ok:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/categorias/{categoria_id}")
def borrar_categoria(categoria_id: str):
    try:
        ok = delete_categoria(categoria_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/categorias")
def listar_categorias():
    return get_all_categorias()


@app.post("/servicios/new")
def crear_servicio(servicio: dict):
    servicio_id = create_servicio(servicio)
    return {"ok": True, "id_servicio": servicio_id}


@app.get("/servicios")
def listar_servicios():
    return get_all_servicios()


@app.get("/servicios/{servicio_id}")
def obtener_servicio(servicio_id: str):
    serv = get_by_id(servicio_id)
    if not serv:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return serv


@app.delete("/servicios/{servicio_id}")
def borrar_servicio(servicio_id: str):
    delete_servicio(servicio_id)
    return {"ok": True}


@app.get("/lugares/servicio/{servicio_id}")
def lugares_por_servicio(servicio_id: str):
    lugares_list = get_by_servicio(servicio_id)

    if not lugares_list:
        raise HTTPException(
            status_code=404,
            detail="No hay lugares asociados a este servicio"
        )

    return lugares_list


@app.post("/lugares/{lugar_id}/servicios/{servicio_id}")
def agregar_servicio_a_lugar(lugar_id: str, servicio_id: str):

    if not exists_lugar(lugar_id):
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    add_servicio(lugar_id, servicio_id)

    return {
        "ok": True,
        "message": "Servicio agregado al lugar"
    }


@app.delete("/lugares/{lugar_id}/servicios/{servicio_id}")
def quitar_servicio_de_lugar(lugar_id: str, servicio_id: str):
    lugar = lugares.find_one({"id": lugar_id})
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    remove_servicio(lugar_id, servicio_id)

    return {"ok": True, "message": "Servicio eliminado del lugar"}


from fastapi import HTTPException

@app.get("/lugares/{lugar_id}/servicios")
def servicios_de_lugar(lugar_id: str):

    lugar = lugares.find_one(
        {"id": lugar_id},
        {"_id": 0}
    )

    if not lugar:
        raise HTTPException(
            status_code=404,
            detail="Lugar no encontrado"
        )

    return lugar.get("servicios", [])


@app.post("/opiniones/new")
def nueva_opinion(data: Opinion):
    opinion = data.dict()
    opinion["id_opinion"] = str(uuid.uuid4())

    try:
        ok = create_opinion(opinion)
        if not ok:
            raise HTTPException(status_code=409, detail="Opinión duplicada")
        return {"id_opinion": opinion["id_opinion"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/opiniones/lugar/{lugar_id}")
def opiniones_por_lugar(lugar_id: str):
    return get_by_lugar(lugar_id)


@app.get("/opiniones/promedios/{lugar_id}")
def promedio_por_lugar(lugar_id: str):

    resultado = get_promedio_by_lugar(lugar_id)

    if not resultado:

        raise HTTPException(
            status_code=404,
            detail="El lugar no tiene opiniones"
        )

    return resultado


@app.delete("/opiniones/{id_opinion}")
def borrar_opinion(id_opinion: str):
    ok = delete_opinion(id_opinion)
    if not ok:
        raise HTTPException(status_code=404, detail="Opinión no encontrada")
    return {"ok": True}