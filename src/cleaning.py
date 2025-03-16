import pandas as pd
from sqlalchemy import create_engine

# Ruta de salida
CLEANED_CSV_PATH = "src/static/xlsx/cleaned_data.csv"
AUDIT_PATH = "src/static/auditoria/cleaning_report.txt"

# Paso 1: Conexión a la base de datos y carga de datos
print("🔹 Cargando los datos desde la base de datos...")
engine = create_engine("sqlite:///src/static/db/ingestion.db")

try:
    df = pd.read_sql("SELECT * FROM launches", engine)
except Exception as e:
    print(f"⚠️ Error al cargar datos desde la base de datos: {e}")
    exit()

# Estado inicial
initial_records = df.shape[0]
print(f"✅ Datos cargados: {initial_records} registros")

# Paso 2: Análisis exploratorio y validación de los datos
print("\n--- 🔍 Análisis Exploratorio ---")
print(f"📌 Registros duplicados: {df.duplicated().sum()}")

# Verificación de valores nulos por columna
print("\n📌 Valores nulos por columna:")
nulos_por_columna = df.isnull().sum()
print(nulos_por_columna)

# Verificación de tipos de datos
print("\n📌 Tipos de datos antes de la limpieza:")
print(df.dtypes)

# Paso 3: Limpieza de los datos
print("\n--- 🛠️ Proceso de Limpieza ---")

# 3.1 Eliminación de duplicados
df = df.drop_duplicates()
after_duplicates = df.shape[0]
print(f"📌 Registros después de eliminar duplicados: {after_duplicates}")

# 3.2 Manejo de valores nulos
df = df.dropna(subset=["success"])
after_nulls = df.shape[0]
print(f"📌 Registros después de eliminar valores nulos en 'success': {after_nulls}")

# Imputar valores nulos en 'details'
df["details"] = df["details"].fillna("No details available")
print(f"📌 Valores nulos imputados en 'details': {df['details'].isnull().sum()}")

# 3.3 Corrección de tipos de datos
try:
    df["date_utc"] = pd.to_datetime(df["date_utc"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    print("✅ Fechas convertidas correctamente")
except Exception as e:
    print(f"⚠️ Error al convertir fechas: {e}")

# Tipos de datos después de la corrección
print("\n📌 Tipos de datos después de la corrección:")
print(df.dtypes)

# Paso 4: Exportar datos limpios a CSV
try:
    df.to_csv(CLEANED_CSV_PATH, index=False)
    print(f"✅ Archivo CSV generado: {CLEANED_CSV_PATH}")
except Exception as e:
    print(f"⚠️ Error al guardar el archivo CSV: {e}")

# Paso 5: Generación del archivo de auditoría
try:
    with open(AUDIT_PATH, "w") as f:
        f.write(f"🔹 Auditoría de Limpieza de Datos\n")
        f.write(f"Fecha y hora: {pd.Timestamp.now()}\n\n")
        f.write(f"📌 Total de registros iniciales: {initial_records}\n")
        f.write(f"📌 Registros eliminados por duplicados: {initial_records - after_duplicates}\n")
        f.write(f"📌 Registros eliminados por valores nulos en 'success': {after_duplicates - after_nulls}\n")
        f.write(f"📌 Valores nulos imputados en 'details': {df['details'].isnull().sum()}\n")
        f.write(f"\n📌 Tipos de datos después de la limpieza:\n{df.dtypes}\n")

    print(f"✅ Informe de auditoría generado en: {AUDIT_PATH}")
except Exception as e:
    print(f"⚠️ Error al generar el informe de auditoría: {e}")
