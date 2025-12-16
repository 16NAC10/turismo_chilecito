import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

OSM_TYPE_MAPPING = {
    "hotel": ['node["tourism"="hotel"]'],
    "hostel": ['node["tourism"="hostel"]'],
    "restaurante": ['node["amenity"="restaurant"]'],
    "comedor": ['node["amenity"="fast_food"]'],
    "bodega": ['node["craft"="winery"]'],
    "atraccion": ['node["tourism"="attraction"]', 'node["tourism"="viewpoint"]', 'node["tourism"="museum"]'],
    "terminal_omnibus": ['node["amenity"="bus_station"]'],
    "parada_colectivo": ['node["highway"="bus_stop"]'],
    "sendero": ['way["route"="hiking"]', 'way["highway"="path"]'],
}

def build_query():
    parts = []
    for queries in OSM_TYPE_MAPPING.values():
        for q in queries:
            parts.append(f"{q}(area.searchArea);")

    return f"""
    [out:json][timeout:25];
    area["name"="Chilecito"]->.searchArea;
    (
        {''.join(parts)}
    );
    out tags center;
    """

def fetch_osm_data():
    response = requests.post(OVERPASS_URL, data=build_query())
    return response.json()["elements"]