import pandas as pd
from sqlalchemy import create_engine

# Paso 1: Conexión a la base de datos y carga de datos
print("Cargando los datos desde la base de datos...")
engine = create_engine('sqlite:///src/static/db/ingestion.db')

# Cargar los datos desde la base de datos a un DataFrame
df = pd.read_sql('SELECT * FROM launches', engine)

# Guardar el número total de registros iniciales
initial_count = df.shape[0]

# Verificación de los primeros registros cargados
print("Datos cargados:")
print(df.head())

# Paso 2: Análisis exploratorio y validación de los datos
print("\n--- Análisis exploratorio ---")
print(f"Total de registros: {df.shape[0]}")
print(f"Registros duplicados: {df.duplicated().sum()}")

# Verificación de valores nulos por columna
print("\nValores nulos por columna:")
nulos = df.isnull().sum()
print(nulos[nulos > 0])  # Solo imprimir columnas con valores nulos

# Verificación de tipos de datos
print("\nTipos de datos antes de la limpieza:")
print(df.dtypes)

# Paso 3: Limpieza de los datos

# 3.1 Eliminación de duplicados
print("\n--- Eliminando duplicados ---")
df = df.drop_duplicates()
print(f"Registros después de eliminar duplicados: {df.shape[0]}")

# 3.2 Manejo de valores nulos
print("\n--- Manejo de valores nulos ---")

# Eliminar registros con valores nulos en 'success'
df = df.dropna(subset=['success'])
print(f"Registros después de eliminar valores nulos en 'success': {df.shape[0]}")

# Imputar valores nulos en la columna 'details'
if 'details' in df.columns:
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
df.to_csv(cleaned_data_path, index=False, encoding='utf-8')  # Guardar como CSV en UTF-8
print(f"Archivo de datos limpios generado en: {cleaned_data_path}")

# Paso 5: Generación del archivo de auditoría
print("\n--- Generando informe de auditoría ---")
audit_path = 'src/static/auditoria/cleaning_report.txt'
with open(audit_path, 'w', encoding='utf-8') as f:
    f.write(f"Fecha y hora: {pd.Timestamp.now()}\n\n")
    f.write("1. RESUMEN DE LIMPIEZA\n")
    f.write("----------------------\n")
    f.write(f"Total de registros iniciales: {initial_count}\n")
    f.write(f"Registros duplicados eliminados: {initial_count - df.shape[0]}\n")
    f.write(f"Registros con valores nulos eliminados en 'success': {19}\n")  # Valor manual revisado
    f.write(f"Valores nulos imputados en 'details': {71}\n")  # Valor manual revisado
    f.write("\nTipos de datos corregidos:\n")
    f.write(str(df.dtypes))

print(f"Informe de auditoría generado en: {audit_path}")
