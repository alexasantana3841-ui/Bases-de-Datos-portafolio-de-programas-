"""Programa 2: limpieza de base de datos (indicadores OECD/Banco Mundial exportados de MongoDB)."""
import pandas as pd

ARCHIVO_ENTRADA = "BancoMundialdb_indicadores.csv"
ARCHIVO_SALIDA = "indicadores_limpio.csv"

df = pd.read_csv(ARCHIVO_ENTRADA)
print("Filas y columnas originales:", df.shape)

# 1. Quitar la columna _id que genera MongoDB
df = df.drop(columns=["_id"])

# 2. Quitar columnas constantes (tienen el mismo valor en todas las filas, no aportan)
constantes = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
df = df.drop(columns=constantes)
print("Columnas constantes eliminadas:", len(constantes))

# 3. Quitar duplicados
duplicados = df.duplicated().sum()
df = df.drop_duplicates()
print("Duplicados eliminados:", duplicados)

# 4. Nulos: las filas sin valor observado no sirven para el análisis
nulos = df["OBS_VALUE"].isna().sum()
print("Nulos en OBS_VALUE:", nulos)
df = df.dropna(subset=["OBS_VALUE"])

# 5. Tipos de datos
df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
df["OBS_VALUE"] = df["OBS_VALUE"].astype(float)
for col in ["REF_AREA", "INDICATOR", "COMP_BREAKDOWN_1", "OBS_STATUS"]:
    df[col] = df[col].astype("category")

# 6. Limpiar texto de las etiquetas
df["INDICATOR_LABEL"] = (
    df["INDICATOR_LABEL"].str.replace("Product Market Regulation (PMR): ", "", regex=False).str.strip()
)

# 7. Valores atípicos: se detectan con IQR por indicador (se reportan, no se borran,
#    porque son valores reales de países con regulaciones muy distintas)
q1 = df.groupby("INDICATOR", observed=True)["OBS_VALUE"].transform(lambda s: s.quantile(0.25))
q3 = df.groupby("INDICATOR", observed=True)["OBS_VALUE"].transform(lambda s: s.quantile(0.75))
iqr = q3 - q1
df["ATIPICO"] = (df["OBS_VALUE"] < q1 - 1.5 * iqr) | (df["OBS_VALUE"] > q3 + 1.5 * iqr)
print("Valores atípicos marcados:", int(df["ATIPICO"].sum()))

# 8. Validar rango: la escala PMR va de 0 a 6
fuera = ((df["OBS_VALUE"] < 0) | (df["OBS_VALUE"] > 6)).sum()
print("Valores fuera de la escala 0-6:", fuera)

print("Filas y columnas finales:", df.shape)
df.to_csv(ARCHIVO_SALIDA, index=False)
print("Guardado en", ARCHIVO_SALIDA)
