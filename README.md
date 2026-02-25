# TURISMO CHILECITO

## Descripción General

**Turismo Chilecito** es un proyecto académico cuyo objetivo es centralizar, gestionar y analizar información turística de la ciudad de Chilecito, La Rioja, utilizando una **base de datos documental (MongoDB)**.

La aplicación permite registrar, consultar y analizar lugares turísticos como:

* Hospedajes
* Restaurantes
* Bodegas
* Senderos
* Transporte
* Atracciones

Los datos pueden cargarse:

* Manualmente
* Importarse desde OpenStreetMap (OSM)

---

## Equipo de Trabajo

**Manuel Ignacio Páez** - 
[ignaciopaez16@gmail.com](mailto:ignaciopaez16@gmail.com)

---

## Funcionalidades principales

### Lugares:

* Importar lugares desde OSM
* Crear lugar
* Modificar lugar
* Eliminar lugar
* Listar lugares
* Buscar lugar por id
* Buscar por tipo
* Buscar por categoría
* Buscar por servicio

---

### Opiniones:

* Crear opinión
* Eliminar opinión
* Listar opiniones por lugar
* Obtener promedio de puntuación por lugar

---

### Servicios:

* Agregar servicio a lugar
* Quitar servicio de lugar
* Listar servicios de un lugar

---

## Tecnologías Utilizadas

Backend:

* Python 3.10+
* FastAPI
* Uvicorn

Base de Datos:

* MongoDB
* PyMongo

API externa:

* OpenStreetMap
* Overpass API

Documentación:

* Swagger

---

## Instalación

### 1️⃣ Requisitos

Instalar:

* Python 3.10+
* MongoDB Community
* Git

Opcional:

* MongoDB Compass

---

### 2️⃣ Clonar repositorio

```bash
cd Desktop
git clone https://github.com/16NAC10/turismo_chilecito.git
cd turismo_chilecito
```

---

### 3️⃣ Crear entorno virtual

```bash
cd backend

python -m venv venv

venv\Scripts\activate
```

---

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Inicializar base de datos

```bash
python db/init_db.py
```

---

### 6️⃣ Ejecutar servidor

```bash
python -m uvicorn app:app --reload
```

---

## Acceder a la API

Swagger:

```
http://localhost:8000/docs
```

---

## Endpoints principales

---

### Lugares

Crear lugar manual:

```
POST /lugares/new
```

Listar lugares:

```
GET /lugares
```

Buscar por id:

```
GET /lugares/{id}
```

Buscar por tipo:

```
GET /lugares/tipo/{tipo}
```

Buscar por categoría:

```
GET /lugares/categoria/{categoria}
```

Eliminar lugar:

```
DELETE /lugares/{id}
```

---

### Servicios

Agregar servicio:

```
POST /lugares/{id}/servicios
```

Eliminar servicio:

```
DELETE /lugares/{id}/servicios/{servicio_id}
```

Listar servicios:

```
GET /lugares/{id}/servicios
```

---

### Opiniones

Crear:

```
POST /opiniones
```

Listar por lugar:

```
GET /opiniones/lugar/{id}
```

Promedio:

```
GET /opiniones/promedio/{id}
```

---

### Importar desde OSM

```
POST /import-osm
```

---

## Base de Datos

Base:

```
turismo
```

Colecciones:

```
lugares
opiniones
servicios
tipos
categorias
```

---

## Diagrama ER

<img width="1870" height="1028" alt="turismo_db" src="https://github.com/user-attachments/assets/90bbd718-813e-4d6f-949d-6738fe4e97be" />

