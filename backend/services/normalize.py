def detect_tipo(tags: dict) -> str:
    if tags.get("tourism") == "hotel":
        return "hotel"
    if tags.get("tourism") == "hostel":
        return "hostel"
    if tags.get("amenity") == "restaurant":
        return "restaurante"
    if tags.get("amenity") == "fast_food":
        return "comedor"
    if tags.get("craft") == "winery":
        return "bodega"
    if tags.get("tourism") in ["attraction", "viewpoint", "museum"]:
        return "atraccion"
    if tags.get("amenity") == "bus_station":
        return "terminal_colectivos"
    if tags.get("highway") == "bus_stop":
        return "parada_colectivo"
    if tags.get("route") == "hiking" or tags.get("highway") == "path":
        return "sendero"
    return "otro"


def detect_categoria(tipo: str) -> str | None:
    categorias = {
        "hotel": "alojamiento",
        "hostel": "alojamiento",
        "restaurante": "gastronomia",
        "comedor": "gastronomia",
        "bodega": "produccion",
        "atraccion": "turismo",
        "sendero": "naturaleza",
        "terminal_omnibus": "transporte",
        "parada_colectivo": "transporte"
    }
    return categorias.get(tipo)

def normalize_nombre(nombre):
    if not nombre:
        return None
    nombre = nombre.strip()
    return nombre if nombre else None

def normalize_osm_element(el: dict) -> dict:
    tags = el.get("tags", {})

    lat = el.get("lat") or el.get("center", {}).get("lat")
    lon = el.get("lon") or el.get("center", {}).get("lon")

    return {
        "osm_id": el["id"],
        "nombre": normalize_nombre(tags.get("name")) or "Sin nombre",
        "tipo_nombre": detect_tipo(tags), 
        "categoria_nombre": detect_categoria(detect_tipo(tags)),
        "lat": lat,
        "lon": lon,
        "servicios": [],
        "source": 'OSM'
    }