import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Tipos de elementos OSM que interesan al proyecto
OSM_QUERIES = [
    'node["tourism"="hotel"]',
    'node["tourism"="hostel"]',
    'node["amenity"="restaurant"]',
    'node["amenity"="fast_food"]',
    'node["craft"="winery"]',
    'node["tourism"="attraction"]',
    'node["tourism"="viewpoint"]',
    'node["tourism"="museum"]',
    'node["amenity"="bus_station"]',
    'node["highway"="bus_stop"]',
    'way["route"="hiking"]',
    'way["highway"="path"]',
]

def build_query(city: str) -> str:
    """
    Construye la consulta Overpass para una ciudad dada
    """
    parts = [f"{q}(area.searchArea);" for q in OSM_QUERIES]

    return f"""
    [out:json][timeout:25];
    area["name"="{city}"]->.searchArea;
    (
        {''.join(parts)}
    );
    out tags center;
    """

def fetch_osm_data(city: str = "Chilecito") -> list:
    """
    Obtiene datos OSM crudos (sin normalizar)
    """
    response = requests.post(
        OVERPASS_URL,
        data=build_query(city)
    )

    response.raise_for_status()

    return response.json().get("elements", [])