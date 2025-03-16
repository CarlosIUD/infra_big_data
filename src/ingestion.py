import os
import json
import sqlite3
import requests
import pandas as pd
from datetime import datetime

# Configuración
BASE_URL = "https://api.spacexdata.com/v4/launches"
DB_PATH = "src/static/db/ingestion.db"
CSV_PATH = "src/static/xlsx/ingestion.csv"  # Cambié el nombre de Excel a CSV
AUDIT_PATH = "src/static/auditoria/ingestion.txt"

def ensure_directories_exist():
    """Asegura que los directorios necesarios existan."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)  # Modificado para CSV
    os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)

def get_launch_data():
    """Obtiene datos de todos los lanzamientos desde la API de SpaceX."""
    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error en la solicitud HTTP: {response.status_code}")
        return None

def create_database():
    """Crea la base de datos SQLite y la tabla de lanzamientos si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla launches
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS launches (
        id TEXT PRIMARY KEY,
        flight_number INTEGER,
        name TEXT,
        date_utc TEXT,
        date_local TEXT,
        success BOOLEAN,
        details TEXT,
        rocket_id TEXT,
        launchpad_id TEXT,
        payloads TEXT,
        ships TEXT,
        capsules TEXT,
        failures TEXT,
        timestamp TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_launch_data(launch_data):
    """Inserta los datos de un lanzamiento en la base de datos."""
    if not launch_data:
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Comprobar si el lanzamiento ya existe
    cursor.execute("SELECT id FROM launches WHERE id = ?", (launch_data.get('id'),))
    if cursor.fetchone():
        print(f"El lanzamiento {launch_data.get('name')} ya existe en la base de datos.")
        conn.close()
        return False
    
    # Insertar lanzamiento
    try:
        cursor.execute('''
        INSERT INTO launches (
            id, flight_number, name, date_utc, date_local, success,
            details, rocket_id, launchpad_id, payloads, ships, capsules,
            failures, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            launch_data.get('id'),
            launch_data.get('flight_number'),
            launch_data.get('name'),
            launch_data.get('date_utc'),
            launch_data.get('date_local'),
            launch_data.get('success'),
            launch_data.get('details'),
            launch_data.get('rocket'),
            launch_data.get('launchpad'),
            json.dumps(launch_data.get('payloads', [])),
            json.dumps(launch_data.get('ships', [])),
            json.dumps(launch_data.get('capsules', [])),
            json.dumps(launch_data.get('failures', [])),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")
        conn.rollback()
        conn.close()
        return False

def generate_csv_sample():
    """Genera un archivo CSV con una muestra de los datos almacenados."""
    conn = sqlite3.connect(DB_PATH)
    
    # Obtener todos los registros de la tabla launches
    query = "SELECT id, flight_number, name, date_utc, success FROM launches"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    # Guardar como CSV
    df.to_csv(CSV_PATH, index=False)  # Cambié to_excel por to_csv
    print(f"Archivo CSV generado en {CSV_PATH}")

def generate_audit_file(api_data, db_data):
    """Genera un archivo de auditoría comparando datos de API vs. base de datos."""
    with open(AUDIT_PATH, 'w', encoding='utf-8') as f:
        f.write("Auditoria\n")
        f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("1. RESUMEN DE INGESTIÓN\n")
        f.write("----------------------\n")
        f.write(f"Total de registros consultados en API: {len(api_data)}\n")
        f.write(f"Total de registros encontrados en API: {sum(1 for d in api_data if d)}\n")
        f.write(f"Total de registros almacenados en BD: {len(db_data)}\n\n")


def get_db_data():
    """Obtiene todos los datos almacenados en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, flight_number, name, date_utc, success 
    FROM launches
    ''')
    
    rows = cursor.fetchall()
    
    # Convertir a lista de diccionarios
    result = [dict(row) for row in rows]
    
    conn.close()
    return result

def main():
    """Función principal del script de ingestión."""
    print("Iniciando proceso de ingestión de datos...")
    
    # Asegurar que los directorios existan
    ensure_directories_exist()
    
    # Crear base de datos
    create_database()
    
    # Obtener datos de API y almacenarlos
    api_data = get_launch_data()
    if api_data:
        for launch in api_data:
            success = insert_launch_data(launch)
            if success:
                print(f"Datos de {launch.get('name')} insertados correctamente")
            else:
                print(f"No se pudieron insertar datos de {launch.get('name')}")
    
    # Obtener datos de la BD para auditoría
    db_data = get_db_data()
    
    # Generar archivo CSV
    generate_csv_sample()  # Llamé al nuevo método para CSV
    
    # Generar archivo de auditoría
    generate_audit_file(api_data, db_data)
    
    print("Proceso de ingestión completado")

if __name__ == "__main__":
    main()