# 🚀 Proyecto Integrador: Preprocesamiento y Limpieza de Datos en Plataforma de Big Data

## 📌 **Descripción del Proyecto**
Este proyecto implementa un pipeline de **ingestión y limpieza de datos** desde la API de SpaceX hacia una base de datos en SQLite, seguido de un proceso de **preprocesamiento y limpieza de datos** para garantizar la calidad de la información.

Los datos se extraen, transforman y validan utilizando Python, Pandas y SQLAlchemy, y se generan **archivos de auditoría** y **datos limpios** en formato CSV. Además, todo el proceso está **automatizado con GitHub Actions**.

## 🏗 **Estructura del Proyecto**
```
nombre_apellido
├── setup.py            # Configuración del paquete
├── README.md           # Documentación del proyecto (este archivo)
├── requirements.txt    # Dependencias del proyecto
├── .github/workflows   # Configuración de GitHub Actions
│   ├── bigdata.yml     # Workflow automatizado
└── src                 # Código fuente
    ├── static          # Archivos generados
    │   ├── auditoria   # Archivos de auditoría
    │   │   └── cleaning_report.txt  # Reporte de auditoría de limpieza
    │   ├── db          # Base de datos SQLite
    │   │   └── ingestion.db  # Base de datos de lanzamientos
    │   └── xlsx        # Archivos CSV generados
    │       ├── ingestion.csv   # Datos sin limpiar
    │       └── cleaned_data.csv  # Datos limpios
    ├── ingestion.py    # Script de ingestión de datos desde la API
    ├── cleaning.py     # Script de preprocesamiento y limpieza de datos
```

## 🛠 **Requisitos Previos**
Para ejecutar este proyecto localmente, necesitas:
- **Python 3.9 o superior**
- **Git**
- **Pandas** (`pip install pandas`)
- **SQLAlchemy** (`pip install sqlalchemy`)
- **Requests** (`pip install requests`)

Instala todas las dependencias con:
```bash
pip install -r requirements.txt
```

## 🔄 **Flujo del Proceso**
1. **Ingesta de Datos (`ingestion.py`)**:
   - Se conecta a la API de SpaceX.
   - Extrae la información de lanzamientos.
   - Almacena los datos en SQLite (`ingestion.db`).
   - Genera un archivo CSV de los datos sin procesar (`ingestion.csv`).

2. **Preprocesamiento y Limpieza (`cleaning.py`)**:
   - Carga los datos desde la base de datos.
   - Realiza un análisis exploratorio (duplicados, valores nulos, tipos de datos).
   - Aplica correcciones y transformaciones necesarias.
   - Exporta los datos limpios a un archivo CSV (`cleaned_data.csv`).
   - Genera un reporte de auditoría (`cleaning_report.txt`).

3. **Automatización con GitHub Actions (`bigdata.yml`)**:
   - Al hacer `push` a `main`, se ejecuta el pipeline automáticamente.
   - Se ejecutan `ingestion.py` y `cleaning.py`.
   - Se suben los archivos generados como artefactos.

## 📊 **Evidencias Generadas**
El proyecto genera los siguientes archivos como prueba de ejecución:
- **`cleaned_data.csv`**: Contiene los datos limpios después del preprocesamiento.
- **`cleaning_report.txt`**: Resumen del proceso de limpieza, detallando los cambios en los datos.

## 🚀 **Cómo Ejecutar el Proyecto Localmente**
Clona el repositorio y navega a la carpeta del proyecto:
```bash
git clone https://github.com/usuario/repo.git
cd repo
```

Ejecuta la ingesta de datos:
```bash
python src/ingestion.py
```

Ejecuta el proceso de limpieza:
```bash
python src/cleaning.py
```

Verifica los archivos generados en `src/static/xlsx` y `src/static/auditoria`.

## 🤖 **Automatización con GitHub Actions**
Este proyecto está completamente automatizado con GitHub Actions. Cada vez que se hace un `push` a `main`:
1. Se configura el entorno Python.
2. Se instalan dependencias.
3. Se ejecuta el pipeline de ingesta y limpieza.
4. Se suben los archivos generados a GitHub.

El archivo de configuración se encuentra en `.github/workflows/bigdata.yml`.

## 📌 **Contacto**
📧 **Carlos Andrés Cardona Quintero** - carlos.cardona@est.iudigital.edu.co
📧 **Mateo Valencia Minota** - mateo.valencia@est.iudigital.edu.co