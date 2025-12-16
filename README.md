# TURISMO CHILECITO

## Descripción General

**Turismo Chilecito** es un proyecto académico cuyo objetivo es centralizar y gestionar información turística de la ciudad de **Chilecito, La Rioja**. La aplicación permite registrar y consultar distintos tipos de lugares turísticos, como **hospedajes, restaurantes, bodegas, senderos, transporte y puntos de interés**, facilitando su visualización y análisis.

El sistema está compuesto por un **backend en Python con FastAPI** y una **base de datos MongoDB**. Los datos pueden cargarse manualmente o importarse desde **OpenStreetMap (OSM)**.

---

## Equipo de Trabajo

* Manuel Ignacio Páez - ignaciopaez16@gmail.com

---

## Funcionalidades Principales

* Alta, baja y modificación de lugares turísticos (ABM)
* Consulta de todos los lugares o filtrados por tipo turístico
* Persistencia de datos en base de datos NoSQL (MongoDB)
* Documentación automática de la API mediante Swagger

---

## Tecnologías Utilizadas

* **Backend:** Python 3, FastAPI, Uvicorn
* **Base de Datos:** MongoDB, PyMongo
* **APIs externas:** OpenStreetMap (Overpass API)

---

## Instalación y Ejecución (Windows)

### 1️⃣ Requisitos

* Python 3.10 o superior
* MongoDB Community Edition
* Git
* MongoDB Compass (opcional)

---

### 2️⃣ Clonar el repositorio

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

Acceder a la documentación de la API:

* [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 4️⃣ Base de Datos (MongoDB)

Iniciar el servicio de MongoDB y verificar la conexión con:

```
mongodb://localhost:27017
```

Base de datos utilizada:

* **turismo**
* Colección: **lugares**

---

## Uso Básico

* Crear lugares: `POST /lugares`
* Consultar lugares: `GET /lugares`
* Filtrar por tipo: `GET /lugares/tipo/{tipo}`
* Modificar lugares: `PUT /lugares/{id}`
* Eliminar lugares: `DELETE /lugares/{id}`

---
