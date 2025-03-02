## Infraestructura para Big Data (Proyecto Integrador - Big Data)

Este proyecto implementa un pipeline de ingestión de datos desde la API de Rest Launches hacia una base de datos en SQLite y se generan evidencias del proceso mediante el uso de procesos básicos de auditoría. 

## Estudiantes
Mateo Valencia Minota.

Carlos Andrés Cardona Quintero.

## Descripción del entrgable

El proyecto extrae información sobre lanzamientos de cohetes de SpaceX desde la API Launches, almacena estos datos en una base de datos SQLite, y genera dos archivos de evidencia:

1. Inserción de registros en SQLite.
2. Un archivo Excel con una muestra de los registros almacenados.
3. Un archivo de auditoría que compara los datos extraídos con los almacenados.
   

Todo el proceso está automatizado mediante GitHub Actions para ejecutarse automáticamente.

## Estructura del proyecto

```
nombre_apellido
├── setup.py            # Configuración del paquete
├── README.md           # Este archivo
├── requirements.txt    # Dependencias del proyecto
├── .github/workflows   # Configuración de GitHub Actions
└── src                 # Código fuente
    ├── static          # Archivos generados
    │   ├── auditoria   # Archivos de auditoría
    │   ├── db          # Base de datos SQLite
    │   └── xlsx        # Archivos Excel generados
    └── ingestion.py    # Script principal de ingestión
```


## Automatización con GitHub Actions

El proceso está completamente automatizado mediante GitHub Actions, permitiendo la ejecución de los test de manera rápida.



## API 

Utilizamos la API de Rest Launches https://api.spacexdata.com/v4/launches
Esta API proporciona datos sobre lanzamientos espaciales. La información incluye:

Fairings: Datos sobre la cofia del cohete (si fue recuperada, reutilizada, etc).

Enlaces: Imágenes del lanzamiento, webcast en YouTube, artículo en Space.com, y página en Wikipedia.

Fechas: Fecha de encendido estático (static_fire_date_utc), fecha de lanzamiento (date_utc), y precisión de la fecha (date_precision).

Cohete: ID del cohete utilizado (rocket).

Resultado del lanzamiento: Indica si fue exitoso (success: false) y detalla fallos (failures).

Detalles del vuelo: Nombre de la misión (name), número de vuelo (flight_number), y descripción del evento (details).

Carga útil: Lista de payloads lanzados.

Lugar de lanzamiento: ID del launchpad utilizado (launchpad).

Información del núcleo del cohete: Si tenía gridfins, patas de aterrizaje, intentos de aterrizaje, etc.


