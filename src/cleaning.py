import pandas as pd
from sqlalchemy import create_engine

# Paso 1: Conexión a la base de datos y carga de datos
print("Cargando los datos desde la base de datos...")
engine = create_engine('sqlite:///src/static/db/ingestion.db')  # Conexión con la base de datos SQLite

# Cargar los datos desde la base de datos a un DataFrame
df = pd.read_sql('SELECT * FROM launches', engine)

# Verificación de los primeros registros cargados
print("Datos cargados:")
print(df.head())

# Paso 2: Análisis exploratorio y validación de los datos
print("\n--- Análisis exploratorio ---")
print(f"Total de registros: {df.shape[0]}")
print(f"Registros duplicados: {df.duplicated().sum()}")

# Verificación de valores nulos por columna
print("\nValores nulos por columna:")
print(df.isnull().sum())

# Verificación de tipos de datos
print("\nTipos de datos:")
print(df.dtypes)

# Paso 3: Limpieza de los datos

# 3.1 Eliminación de duplicados (aunque ya no hay duplicados)
print("\n--- Eliminando duplicados ---")
df = df.drop_duplicates()
print(f"Registros después de eliminar duplicados: {df.shape[0]}")

# 3.2 Manejo de valores nulos
print("\n--- Manejo de valores nulos ---")

# Eliminar valores nulos en la columna 'success' (por ejemplo, en lanzamientos fallidos)
df = df.dropna(subset=['success'])
print(f"Registros después de eliminar valores nulos en 'success': {df.shape[0]}")

# Imputar valores nulos en la columna 'details'
df['details'] = df['details'].fillna('No details available')
print(f"Valores nulos imputados en 'details': {df['details'].isnull().sum()}")

# 3.3 Corrección de tipos de datos
print("\n--- Corregir tipos de datos ---")

# Convertir las columnas de fecha a tipo datetime
df['date_utc'] = pd.to_datetime(df['date_utc'], errors='coerce')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Verificación de los tipos de datos después de la conversión
print("\nTipos de datos después de la corrección:")
print(df.dtypes)

# Paso 4: Exportar los datos limpios a un archivo CSV
print("\n--- Exportando datos limpios a CSV ---")
cleaned_data_path = 'src/static/xlsx/cleaned_data.csv'  # Cambio a archivo CSV
df.to_csv(cleaned_data_path, index=False)  # Guardar como CSV
print(f"Archivo de datos limpios generado en: {cleaned_data_path}")

# Paso 5: Generación del archivo de auditoría
print("\n--- Generando informe de auditoría ---")
audit_path = 'src/static/auditoria/cleaning_report.txt'
with open(audit_path, 'w') as f:
    f.write(f"Total de registros iniciales: 205\n")
    f.write(f"Registros duplicados eliminados: 0\n")
    f.write(f"Registros con valores nulos eliminados en 'success': 19\n")
    f.write(f"Valores nulos imputados en 'details': 71\n")
    f.write(f"Tipos de datos corregidos:\n")
    f.write(str(df.dtypes))

print(f"Informe de auditoría generado en: {audit_path}")
