import pandas as pd
from sqlalchemy import create_engine

# Paso 1: Conexión a la base de datos y carga de datos
print("Cargando los datos desde la base de datos...")
engine = create_engine('sqlite:///src/static/db/ingestion.db')
df = pd.read_sql('SELECT * FROM launches', engine)

# Guardar estado inicial para auditoría
initial_records = df.shape[0]

# Verificación de los primeros registros cargados
print("Datos cargados:")
print(df.head())

# Paso 2: Análisis exploratorio y validación de los datos
print("\n--- Análisis exploratorio ---")
print(f"Total de registros iniciales: {initial_records}")
print(f"Registros duplicados: {df.duplicated().sum()}")

# Verificación de valores nulos por columna
print("\nValores nulos por columna:")
nulos_por_columna = df.isnull().sum()
print(nulos_por_columna)

# Verificación de tipos de datos
print("\nTipos de datos antes de la limpieza:")
print(df.dtypes)

# Paso 3: Limpieza de los datos
print("\n--- Eliminando duplicados ---")
df = df.drop_duplicates()
after_duplicates = df.shape[0]
print(f"Registros después de eliminar duplicados: {after_duplicates}")

print("\n--- Manejo de valores nulos ---")
df = df.dropna(subset=['success'])
after_nulls = df.shape[0]
print(f"Registros después de eliminar valores nulos en 'success': {after_nulls}")

df['details'] = df['details'].fillna('No details available')
print(f"Valores nulos imputados en 'details': {df['details'].isnull().sum()}")

# Conversión de fechas
df['date_utc'] = pd.to_datetime(df['date_utc'], errors='coerce')
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

print("\nTipos de datos después de la corrección:")
print(df.dtypes)

# Exportar datos limpios a CSV
cleaned_data_path = 'src/static/xlsx/cleaned_data.csv'
df.to_csv(cleaned_data_path, index=False)
print(f"Archivo CSV de datos limpios generado en: {cleaned_data_path}")

# Generar informe de auditoría
audit_path = 'src/static/auditoria/cleaning_report.txt'
with open(audit_path, 'w') as f:
    f.write(f"Total de registros iniciales: {initial_records}\n")
    f.write(f"Registros duplicados eliminados: {initial_records - after_duplicates}\n")
    f.write(f"Registros con valores nulos eliminados en 'success': {after_duplicates - after_nulls}\n")
    f.write(f"Valores nulos imputados en 'details': {df['details'].isnull().sum()}\n")
    f.write("Tipos de datos después de la corrección:\n")
    f.write(str(df.dtypes))

print(f"Informe de auditoría generado en: {audit_path}")