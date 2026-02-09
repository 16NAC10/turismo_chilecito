# TURISMO CHILECITO

## Descripción General

**Turismo Chilecito** es un proyecto académico cuyo objetivo es centralizar, normalizar y gestionar información turística de la ciudad de **Chilecito, La Rioja (Argentina)**. La aplicación permite registrar, consultar y analizar distintos tipos de lugares turísticos —como hospedajes, restaurantes, bodegas, senderos, transporte y puntos de interés— facilitando su organización y futura visualización.

El sistema está compuesto por un **backend en Python con FastAPI** y una **base de datos NoSQL MongoDB**. Los datos pueden cargarse **manualmente** o importarse desde **OpenStreetMap (OSM)** mediante la Overpass API, aplicando procesos de normalización y control de duplicados.

---

## Equipo de Trabajo

* **Manuel Ignacio Páez**
  📧 [ignaciopaez16@gmail.com](mailto:ignaciopaez16@gmail.com)

---

## Funcionalidades Principales

* Alta, baja y modificación (ABM) de lugares turísticos
* Consulta de lugares turísticos

  * Listado completo
  * Filtrado por tipo y categoría
* Gestión de tipos, categorías, servicios y opiniones de los lugares
* Asociación de servicios a lugares
* Importación de datos desde OpenStreetMap (OSM)
* Persistencia en base de datos NoSQL (MongoDB)
* Validaciones de datos y manejo de excepciones
* Documentación automática de la API mediante **Swagger / OpenAPI**

---

## Arquitectura General

* **Backend**: API REST desarrollada con FastAPI
* **Base de datos**: MongoDB
* **Modelo de datos**:

  * Lugares
  * Tipos
  * Categorías
  * Servicios
  * Opiniones
* **Origen de datos**:

  * Manual (`source = MANUAL`)
  * OpenStreetMap (`source = OSM`)

Se utilizan **índices parciales y únicos** para evitar duplicados provenientes de OSM sin afectar los registros creados manualmente.

---

## Tecnologías Utilizadas

* **Lenguaje**: Python 3.10+
* **Framework Backend**: FastAPI
* **Servidor ASGI**: Uvicorn
* **Base de Datos**: MongoDB
* **Driver MongoDB**: PyMongo
* **API Externa**: OpenStreetMap (Overpass API)

---

## Instalación y Ejecución (Windows)

### 1️⃣ Requisitos Previos

* Python 3.10 o superior
* MongoDB Community Edition
* Git
* MongoDB Compass (opcional, para administración visual)

---

### 2️⃣ Clonar el Repositorio

```bash
cd Desktop
git clone https://github.com/16NAC10/turismo_chilecito.git
cd turismo_chilecito
```

---

### 3️⃣ Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Acceder a la documentación interactiva de la API (Swagger UI):

* [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 4️⃣ Base de Datos (MongoDB)

Asegurarse de que el servicio de MongoDB esté iniciado:

```text
mongodb://localhost:27017
```

Base de datos utilizada:

* **Nombre**: `turismo`
* **Colecciones principales**:

  * `lugares`
  * `tipos`
  * `categorias`
  * `servicios`
  * `opiniones`

El proyecto incluye un script de inicialización que crea automáticamente las colecciones y sus índices:

```bash
python backend/db/init_db.py
```

---

## Índices y Consistencia de Datos

* Índices únicos para evitar duplicados de tipos, categorías y servicios
* Índice único parcial sobre `osm_id` en lugares:

  * Garantiza que los lugares importados desde OSM no se dupliquen
  * Permite múltiples lugares creados manualmente sin `osm_id`

---

## Diagrama ER

<img width="1351" height="948" alt="turismo_db" src="https://github.com/user-attachments/assets/a4a4bf72-8256-4978-8b0b-8179605da2bd" />

