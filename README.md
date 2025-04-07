# 🚀 Proyecto Integrador: Preprocesamiento, Limpieza y Enriquecimiento de Datos en Plataforma de Big Data

## 📌 **Descripción del Proyecto**
Este proyecto implementa un pipeline de **ingestión, limpieza y enriquecimiento de datos** con datos de startups unicornio. A partir de una fuente base en formato CSV y un dataset complementario en JSONL, se generan múltiples archivos complementarios (JSON, CSV, TXT) y se combinan en un **dataset enriquecido**. Todo el proceso es **automatizado con GitHub Actions**.

## 🏗 **Estructura del Proyecto**
```
nombre_apellido
├── setup.py
├── README.md
├── requirements.txt
├── .github/workflows
│   └── bigdata.yml         # Automatización del pipeline completo
└── src
    ├── static
    │   ├── auditoria
    │   │   └── cleaning_report.txt  # Reporte de limpieza
    │   ├── db
    │   │   └── ingestion.db         # Base de datos SQLite
    │   └── xlsx
    │       ├── ingestion.csv        # Datos crudos
    │       └── cleaned_data.csv     # Datos limpios
    ├── ingestion.py
    ├── cleaning.py
    └── enrichment.py               # Enriquecimiento de datos
    ├── docs
│   └── arquitectura_modelo.pdf  # Documento final que describe y explica la arquitectura.
├── data
│   ├── founders.json               # Datos JSON complementarios
│   ├── headcount.csv              # Datos CSV complementarios
│   ├── descriptions.txt           # Descripciones en TXT
│   ├── enriched_data.csv          # Dataset enriquecido
│   └── enrichment_report.txt      # Reporte de auditoría de enriquecimiento
```

## 🛠 **Requisitos Previos**
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
1. **Ingesta de Datos (`ingestion.py`)**
   - Conecta a la API de SpaceX.
   - Guarda datos en SQLite (`ingestion.db`).
   - Exporta a `ingestion.csv`.

2. **Limpieza de Datos (`cleaning.py`)**
   - Lee datos desde SQLite.
   - Corrige duplicados, tipos y valores nulos.
   - Exporta `cleaned_data.csv` y `cleaning_report.txt`.

3. **Enriquecimiento de Datos (`enrichment.py`)**
   - Carga el dataset base y filtra el top 100 por valoración.
   - Genera archivos complementarios en JSON, CSV y TXT.
   - Realiza joins por empresa y crea `enriched_data.csv`.
   - Genera `enrichment_report.txt` con auditoría.

4. **Automatización con GitHub Actions**
   - Ejecuta automáticamente todo el pipeline al hacer `push`.

## 📊 **Evidencias Generadas**
- `cleaned_data.csv` — Datos limpios
- `cleaning_report.txt` — Auditoría de limpieza
- `enriched_data.csv` — Datos enriquecidos
- `enrichment_report.txt` — Auditoría de enriquecimiento

## 🚀 **Ejecución Local del Proyecto**
```bash
git clone https://github.com/usuario/repo.git
cd repo

python src/ingestion.py
python src/cleaning.py
python src/enrichment.py
```

Archivos generados:
- `src/static/xlsx/*.csv`
- `src/static/auditoria/*.txt`
- `data/*.json`, `data/*.csv`, `data/*.txt`

## 🤖 **Automatización con GitHub Actions**
Cada vez que haces `push` a `main`:
- Se crea el entorno y se instalan dependencias
- Se ejecutan `ingestion.py`, `cleaning.py`, `enrichment.py`
- Se suben los archivos generados como artefactos

Configurado en: `.github/workflows/bigdata.yml`

## 📌 **Contacto**

| Nombre                         | Correo Electrónico                              |
|-------------------------------|--------------------------------------------------|
| Carlos Andrés Cardona Quintero | carlos.cardona@est.iudigital.edu.co             |
| Mateo Valencia Minota         | mateo.valencia@est.iudigital.edu.co              |
