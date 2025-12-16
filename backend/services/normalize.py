from services.osm_service import OSM_TYPE_MAPPING

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
        return "terminal_omnibus"
    if tags.get("highway") == "bus_stop":
        return "parada_colectivo"
    if tags.get("route") == "hiking" or tags.get("highway") == "path":
        return "sendero"
    return "otro"

def normalize_osm_element(el):
    lat = el.get("lat") or el.get("center", {}).get("lat")
    lon = el.get("lon") or el.get("center", {}).get("lon")

    return {
        "id": el["id"],
        "nombre": el.get("tags", {}).get("name", "Sin nombre"),
        "tipo": detect_tipo(el.get("tags", {})),
        "lat": lat,
        "lon": lon
    }
