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


def normalize_osm_element(el):

    tags = el.get("tags", {})

    lat = el.get("lat") or el.get("center", {}).get("lat")
    lon = el.get("lon") or el.get("center", {}).get("lon")

    osm = {}

    def add_if_exists(key, value):

        if value is not None and value != "":
            osm[key] = value

    add_if_exists("tourism", tags.get("tourism"))
    add_if_exists("amenity", tags.get("amenity"))
    add_if_exists("phone", tags.get("phone"))
    add_if_exists("email", tags.get("email"))
    add_if_exists("website", tags.get("website"))
    add_if_exists("opening_hours", tags.get("opening_hours"))
    add_if_exists("description", tags.get("description"))

    address = {}

    if tags.get("addr:city"):
        address["city"] = tags.get("addr:city")

    if tags.get("addr:street"):
        address["street"] = tags.get("addr:street")

    if tags.get("addr:housenumber"):
        address["number"] = tags.get("addr:housenumber")

    if address:
        osm["address"] = address

    lugar = {

        "osm_id": el["id"],
        "nombre": tags.get("name", "Sin nombre"),
        "tipo_nombre": detect_tipo(tags),
        "categoria_nombre": detect_categoria(detect_tipo(tags)),
        "lat": lat,
        "lon": lon,
        "servicios": [],
        "source": "OSM"
    }

    if len(osm) > 0:
        lugar["osm"] = osm

    return lugar